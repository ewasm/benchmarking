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

# output paths should be mounted docker volumes
RESULT_CSV_OUTPUT_PATH = "/evmraceresults"

RESULT_CSV_FILENAME = "parity_precompile_benchmarks.csv"

PARITY_DIR = "/parity"

PARITY_PRECOMPILE_BENCH_CMD = "cargo bench --package ethcore --color never"



"""
Benchmarking modexp_nagydani_4_square
Benchmarking modexp_nagydani_4_square: Warming up for 3.0000 s
Benchmarking modexp_nagydani_4_square: Collecting 100 samples in estimated 5.3360 s (71k iterations)
Benchmarking modexp_nagydani_4_square: Analyzing
modexp_nagydani_4_square
                        time:   [74.530 us 75.376 us 76.310 us]
                        change: [-4.2962% -1.7062% +0.7488%] (p = 0.20 > 0.05)
                        No change in performance detected.
Found 7 outliers among 100 measurements (7.00%)
  4 (4.00%) high mild
  3 (3.00%) high severe

Benchmarking modexp_nagydani_4_qube
Benchmarking modexp_nagydani_4_qube: Warming up for 3.0000 s
Benchmarking modexp_nagydani_4_qube: Collecting 100 samples in estimated 5.1062 s (35k iterations)
Benchmarking modexp_nagydani_4_qube: Analyzing
modexp_nagydani_4_qube  time:   [145.48 us 147.36 us 149.49 us]
                        change: [-3.3057% -0.8724% +1.4027%] (p = 0.49 > 0.05)
                        No change in performance detected.
Found 1 outliers among 100 measurements (1.00%)
  1 (1.00%) high mild

Benchmarking modexp_nagydani_4_pow0x10001
Benchmarking modexp_nagydani_4_pow0x10001: Warming up for 3.0000 s
Benchmarking modexp_nagydani_4_pow0x10001: Collecting 100 samples in estimated 6.0989 s (5050 iterations)
Benchmarking modexp_nagydani_4_pow0x10001: Analyzing
modexp_nagydani_4_pow0x10001
                        time:   [1.2012 ms 1.2129 ms 1.2260 ms]
                        change: [-0.8848% +0.7336% +2.5488%] (p = 0.41 > 0.05)
                        No change in performance detected.
Found 3 outliers among 100 measurements (3.00%)
  2 (2.00%) high mild
  1 (1.00%) high severe
"""

def parse_parity_bench_output(stdoutlines):
    nameRegex = "Benchmarking (\w+): Warming up for"
    timeRegex = "time:\s+\[[\d\.]+\s+\w+\s+([\d\.]+\s+\w+)"

    # first match test name
    # then match time, then append result and wait for next test name
    bench_tests = []
    test_name = ""
    bench_time = None
    for line in stdoutlines:
        matchName = re.search(nameRegex, line)
        if matchName:
            test_name = matchName.group(1)
            bench_time = None

        matchTime = re.search(timeRegex, line)
        if matchTime:
            bench_time = matchTime.group(1)
            bench_time = bench_time.replace(" ", "") # "1.2129 ms" -> "1.2129ms"

        if bench_time is not None and test_name != "":
            bench_time = durationpy.from_str(bench_time)
            bench_tests.append({'name': test_name, 'gas': 0, 'time': bench_time.total_seconds()})
            print("parsed test result:", bench_tests[-1])
            bench_time = 0
            test_name = ""

    return bench_tests


def do_parity_precompile_bench():
    # TODO: running `cargo bench` for the first time generates a lot of compiler output.
    # should we do anything to handle that?
    parity_cmd = shlex.split(PARITY_PRECOMPILE_BENCH_CMD)
    print("running parity precompile benchmarks...\n{}".format(PARITY_PRECOMPILE_BENCH_CMD))

    raw_stdoutlines = []
    with subprocess.Popen(parity_cmd, cwd=PARITY_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout: # b'\n'-separated lines
            print(line, end='')
            raw_stdoutlines.append(line)  # pass bytes as is
        p.wait()

    print("process done.  got stdout:", raw_stdoutlines)
    return raw_stdoutlines


def saveResults(precompile_benchmarks):
    result_file = os.path.join(RESULT_CSV_OUTPUT_PATH, RESULT_CSV_FILENAME)

    # back up existing result csv file
    if os.path.isfile(result_file):
        ts = time.time()
        date_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        ts_folder_name = "backup-{}-{}".format(date_str, round(ts))
        dest_backup_path = os.path.join(RESULT_CSV_OUTPUT_PATH, ts_folder_name)
        os.makedirs(dest_backup_path)
        shutil.move(result_file, dest_backup_path)
        print("existing {} moved to {}".format(RESULT_CSV_FILENAME, dest_backup_path))

    with open(result_file, 'w', newline='') as bench_result_file:
        fieldnames = ['test_name', 'gas', 'time']
        writer = csv.DictWriter(bench_result_file, fieldnames=fieldnames)
        writer.writeheader()
        for test_result in precompile_benchmarks:
            writer.writerow({"test_name" : test_result['name'], "gas" : test_result['gas'], "time" : test_result['time']})


def main():
    bench_output = do_parity_precompile_bench()
    bench_results = parse_parity_bench_output(bench_output)
    print("got parity precompile benchmarks:", bench_results)

    ## TODO: bench parity precompiles

    saveResults(bench_results)


if __name__ == "__main__":
    main()