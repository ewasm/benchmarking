#!/usr/bin/env python3

import re
import subprocess
import nanodurationpy as durationpy
import csv
import time
import datetime
import os
import shutil
import shlex
import json

# output paths should be mounted docker volumes
RESULT_CSV_OUTPUT_PATH = "/evmraceresults"

RESULT_CSV_FILENAME = "evm_benchmarks_evmone384.csv"

EVMONE_BENCH_INFOS = [
  {
    "command": "/root/evmone-evm384-v1/build/bin/evmone-bench --benchmark_format=json --benchmark_color=false --benchmark_min_time=5 /root/evm384_f6m_mul/build/v1-f6m_mul_bench.hex 00 74229fc665e6c3f4401905c1a454ea57c8931739d05a074fd60400f19684d680a9e1305c25f13613dcc6cdd6e6e57d0800000000000000000000000000000000",
    "bench_name": "evm384-synth-loop-v1"
  },
  {
    "command": "/root/evmone-evm384-v2/build/bin/evmone-bench --benchmark_format=json --benchmark_color=false --benchmark_min_time=5 /root/evm384_f6m_mul/build/v2-f6m_mul_bench.hex 00 74229fc665e6c3f4401905c1a454ea57c8931739d05a074fd60400f19684d680a9e1305c25f13613dcc6cdd6e6e57d0800000000000000000000000000000000",
    "bench_name": "evm384-synth-loop-v2"
  },
  {
    "command": "/root/evmone-evm384-v3/build/bin/evmone-bench --benchmark_format=json --benchmark_color=false --benchmark_min_time=5 /root/evm384_f6m_mul/build/v3-f6m_mul_bench.hex 00 74229fc665e6c3f4401905c1a454ea57c8931739d05a074fd60400f19684d680a9e1305c25f13613dcc6cdd6e6e57d0800000000000000000000000000000000",
    "bench_name": "evm384-synth-loop-v3"
  },
  {
    "command": "/root/evmone-evm384-v4/build/bin/evmone-bench --benchmark_format=json --benchmark_color=false --benchmark_min_time=5 /root/evm384_f6m_mul/build/v4-f6m_mul_bench.hex 00 74229fc665e6c3f4401905c1a454ea57c8931739d05a074fd60400f19684d680a9e1305c25f13613dcc6cdd6e6e57d0800000000000000000000000000000000",
    "bench_name": "evm384-synth-loop-v4"
  },
  {
    "command": "/root/evmone-evm384-v5/build/bin/evmone-bench --benchmark_format=json --benchmark_color=false --benchmark_min_time=5 /root/evm384_f6m_mul/build/v5-f6m_mul_bench.hex 00 3eb4cfbedd75a21a29701b4f4672232c52318353acdeef6d435d19a2681e023d153b8d400893da3b1525258aa820610e00000000000000000000000000000000",
    "bench_name": "evm384-synth-loop-v5"
  },
  {
    "command": "/root/evmone-evm384-v6/build/bin/evmone-bench --benchmark_format=json --benchmark_color=false --benchmark_min_time=5 /root/evm384_f6m_mul/build/v6-f6m_mul_bench.hex 00 ff",
    "bench_name": "evm384-synth-loop-v6"
  }
]


"""
root@472ab2fd1fc1:~/evm384_f6m_mul# /root/evmone-evm384-v2/build/bin/evmone-bench ~/evm384_f6m_mul/build/v2-f6m_mul_bench.bin "00" "74229fc665e6c3f4401905c1a454ea57c8931739d05a074fd60400f19684d680a9e1305c25f13613dcc6cdd6e6e57d0800000000000000000000000000000000"
Benchmarking evmone

2020-06-18 20:52:56
Running /root/evmone-evm384-v2/build/bin/evmone-bench
Run on (4 X 2294.68 MHz CPU s)
CPU Caches:
  L1 Data 32K (x2)
  L1 Instruction 32K (x2)
  L2 Unified 256K (x2)
  L3 Unified 51200K (x2)
-------------------------------------------------------------------------------------------------------
Benchmark                                                Time           CPU Iterations UserCounters...
-------------------------------------------------------------------------------------------------------
/root/evm384_f6m_mul/build/v2-f6m_mul_bench.bin      18156 us      18156 us         39 gas_rate=322.266M/s gas_used=5.85118M
"""


def do_evmone_bench(evmone_bench_cmd):
    evmone_cmd = shlex.split(evmone_bench_cmd)
    print("running evmone benchmark...\n{}".format(evmone_bench_cmd))

    stdoutlines = []
    with subprocess.Popen(evmone_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout: # b'\n'-separated lines
            print(line, end='')
            stdoutlines.append(line)  # pass bytes as is
        p.wait()

    json_result = json.loads("".join(stdoutlines[2:]))
    benchmarks = json_result['benchmarks']
    benchmark_results = benchmarks[0]
    gasused = int(benchmark_results['gas_used'])
    total_time = str(benchmark_results['real_time']) + benchmark_results['time_unit']
    time = durationpy.from_str(total_time)
    return {'gas_used': gasused, 'time': time.total_seconds()}


def saveResults(precompile_benchmarks):
    # move existing csv file to backup-datetime-folder
    ts = time.time()
    date_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    ts_folder_name = "backup-{}-{}".format(date_str, round(ts))
    dest_backup_path = os.path.join(RESULT_CSV_OUTPUT_PATH, ts_folder_name)
    result_file = "{}/{}".format(RESULT_CSV_OUTPUT_PATH, RESULT_CSV_FILENAME)

    # back up existing result csv file
    if os.path.isfile(result_file):
        os.makedirs(dest_backup_path)
        shutil.move(result_file, dest_backup_path)
        print("existing {} moved to {}".format(RESULT_CSV_FILENAME, dest_backup_path))

    with open(result_file, 'w', newline='') as bench_result_file:
        fieldnames = ['engine', 'test_name', 'total_time', 'gas_used']
        writer = csv.DictWriter(bench_result_file, fieldnames=fieldnames)
        writer.writeheader()
        for test_result in precompile_benchmarks:
            writer.writerow({"engine": test_result['engine'], "test_name" : test_result['bench_name'], "gas_used" : test_result['gas_used'], "total_time" : test_result['time']})



def main():
    all_bench_resuls = []
    for evmone_bench_info in EVMONE_BENCH_INFOS:
      evmone_cmd = evmone_bench_info['command']
      bench_result = do_evmone_bench(evmone_cmd)
      bench_result['bench_name'] = evmone_bench_info['bench_name']
      bench_result['engine'] = "evmone384"
      all_bench_resuls.append(bench_result)

    saveResults(all_bench_resuls)


if __name__ == "__main__":
    main()
