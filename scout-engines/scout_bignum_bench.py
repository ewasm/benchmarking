#!/usr/bin/python

import json, re
import subprocess
import nanodurationpy as durationpy
import csv
import time
import datetime
import os
import shutil
import shlex
import sys
import yaml

# docker run --privileged=true -v $(pwd)/../benchmark_results_data:/benchmark_results_data:cached --security-opt seccomp=unconfined -it scout-engines /bin/bash
RESULT_CSV_OUTPUT_DIR = "/benchmark_results_data"

RESULT_CSV_FILE_NAME = "scout_bignum_benchmarks.csv"

# TODO
# grep -E '^model name|^cpu MHz' /proc/cpuinfo > /benchmark_results_data/cpuinfo.txt



# the wabt branch reads input data from a file in the working directory `./test_block_data.hex`
# we'll create a new directory using bench_name + engine_name, and create test_block_data.hex in each one
WABT_BENCH_WORKING_DIR = "/engines/wabt-bench-dirs"

# because wabt reads input data from `./test_block_data.hex` in the working directory,
# we can execute `wabt_bin_path` from any directory.


# TODO: use scout wabt branch without bignums for the no-bignum runs?
WABT_BENCH_INFOS = [
  {
    'bench_name': 'ecrecover-eth1-txns-websnark-secp256k1-verify-72-sigs',
    'engine_name': 'wabt-with-bignums',
    'wabt_bin_path': '/engines/wabt-secp/out/clang/Release/benchmark-interp',
    'yaml_file_dir': '/scoutyamls/scout.ts-secp/',
    'yaml_file_rel_path': 'secpsigverify.yaml'
  },
  {
    'bench_name': 'ecrecover-eth1-txns-websnark-secp256k1-verify-72-sigs',
    'engine_name': 'wabt-no-bignums',
    'wabt_bin_path': '/engines/wabt-secp/out/clang/Release/benchmark-interp',
    'yaml_file_dir': '/scoutyamls/scout.ts-secp/',
    'yaml_file_rel_path': 'secpsigverify_nobignums.yaml'
  },
  {
    'bench_name': 'ecpairing-zkrollup-websnark-bn128-two-pairings',
    'engine_name': 'wabt-with-bignums',
    'wabt_bin_path': '/engines/wabt-bn128/out/clang/Release/benchmark-interp',
    'yaml_file_dir': '/scoutyamls/scout.ts-bn128/',
    'yaml_file_rel_path': 'bn128pairing_bignums.yaml'
  },
  {
    'bench_name': 'ecpairing-zkrollup-websnark-bn128-two-pairings',
    'engine_name': 'wabt-no-bignums',
    'wabt_bin_path': '/engines/wabt-bn128/out/clang/Release/benchmark-interp',
    'yaml_file_dir': '/scoutyamls/scout.ts-bn128/',
    'yaml_file_rel_path': 'bn128pairing.yaml'
  },
  {
    'bench_name': 'biturbo-token-eth1-mainnet-stateless-block-hexary-trie-keccak256-multiproof',
    'engine_name': 'wabt-biturbo',
    'wabt_bin_path': '/engines/wabt-biturbo/out/clang/Release/benchmark-interp',
    'yaml_file_dir': '/scoutyamls/biturbo/',
    'yaml_file_rel_path': 'turbo-token-realistic.yaml'
  }
]



# use wabt/wasm-interp instead of wabt/benchmark-interp
# benchmark-interp loops over calls to main() without zeroing out memory or re-instantiating the wasm instance
# some wasm modules support repeated calls to main(). Daiqiuri doesn't, so use wasm-interp instead of benchmark-interp
WABT_BENCH_MANUAL_INFOS = [
  {
    'bench_name': 'daiquiri-zkmixer-websnark-bn128-groth16-four-pairings-and-mimc',
    'engine_name': 'wabt-with-bignums',
    'wabt_bin_path': '/engines/wabt-bn128/out/clang/Release/wasm-interp',
    'yaml_file_dir': '/scoutyamls/daiquiri/',
    'yaml_file_rel_path': 'tests/tests-withdraw-bn.yml'
  },
  {
    'bench_name': 'daiquiri-zkmixer-websnark-bn128-groth16-four-pairings-and-mimc',
    'engine_name': 'wabt-no-bignums',
    'wabt_bin_path': '/engines/wabt-bn128/out/clang/Release/wasm-interp',
    'yaml_file_dir': '/scoutyamls/daiquiri/',
    'yaml_file_rel_path': 'tests/tests-withdraw.yml'
  }
]



SCOUTCPP_BENCH_INFOS = [
  {
    'bench_name': 'ecrecover-eth1-txns-websnark-secp256k1-verify-72-sigs',
    'engine_name': 'scoutcpp-with-bignums',
    'scoutcpp_bin_path': '/engines/scoutcpp-secp/build/scout.exec',
    'yaml_working_dir': '/scoutyamls/scout.ts-secp/',
    'yaml_file_path': 'secpsigverify.yaml'
  },
  {
    'bench_name': 'ecrecover-eth1-txns-websnark-secp256k1-verify-72-sigs',
    'engine_name': 'scoutcpp-no-bignums',
    'scoutcpp_bin_path': '/engines/scoutcpp-secp/build/scout.exec',
    'yaml_working_dir': '/scoutyamls/scout.ts-secp/',
    'yaml_file_path': 'secpsigverify_nobignums.yaml'
  },
  {
    'bench_name': 'ecpairing-zkrollup-websnark-bn128-two-pairings',
    'engine_name': 'scoutcpp-with-bignums',
    'scoutcpp_bin_path': '/engines/scoutcpp-bn128/build/scout.exec',
    'yaml_working_dir': '/scoutyamls/scout.ts-bn128/',
    'yaml_file_path': 'bn128pairing_bignums.yaml'
  },
  {
    'bench_name': 'ecpairing-zkrollup-websnark-bn128-two-pairings',
    'engine_name': 'scoutcpp-no-bignums',
    'scoutcpp_bin_path': '/engines/scoutcpp-bn128/build/scout.exec',
    'yaml_working_dir': '/scoutyamls/scout.ts-bn128/',
    'yaml_file_path': 'bn128pairing.yaml'
  },
  {
    'bench_name': 'daiquiri-zkmixer-websnark-bn128-groth16-four-pairings-and-mimc',
    'engine_name': 'scoutcpp-with-bignums',
    'scoutcpp_bin_path': '/engines/scoutcpp-bn128/build/scout.exec',
    'yaml_working_dir': '/scoutyamls/daiquiri/',
    'yaml_file_path': 'tests/tests-withdraw-bn.yml'
  },
  {
    'bench_name': 'daiquiri-zkmixer-websnark-bn128-groth16-four-pairings-and-mimc',
    'engine_name': 'scoutcpp-no-bignums',
    'scoutcpp_bin_path': '/engines/scoutcpp-bn128/build/scout.exec',
    'yaml_working_dir': '/scoutyamls/daiquiri/',
    'yaml_file_path': 'tests/tests-withdraw.yml'
  }
]


# v8 is always benched with no bignums.
# bignums cause a slowdown due to v8's host function overhead
# in practice, wasm engines that don't support the bignum host functions
# could use "polyfill" implementations of the host functions, provided in wasm
# these v8 benchmarks demonstrate using websnark's implementations of bigints
# and modular arithmetic as the polyfill.

# TODO: add v8-interpreter
V8_BENCH_INFOS = [
  {
    'bench_name': 'ecrecover-eth1-txns-websnark-secp256k1-verify-72-sigs',
    'engine_name': 'v8-turbofan',
    'scoutts_cmd': 'npm run start:turbofan secpsigverify_nobignums.yaml',
    'scoutts_working_dir': '/scoutyamls/scout.ts-bn128/'
  },
  {
    'bench_name': 'ecrecover-eth1-txns-websnark-secp256k1-verify-72-sigs',
    'engine_name': 'v8-liftoff',
    'scoutts_cmd': 'npm run start:liftoff secpsigverify_nobignums.yaml',
    'scoutts_working_dir': '/scoutyamls/scout.ts-secp/',
  },
  {
    'bench_name': 'ecrecover-eth1-txns-websnark-secp256k1-verify-72-sigs',
    'engine_name': 'v8-interpreter',
    'scoutts_cmd': 'node --wasm-interpret-all ./dist/cli.js secpsigverify_nobignums.yaml',
    'scoutts_working_dir': '/scoutyamls/scout.ts-secp/',
  },
  {
    'bench_name': 'ecpairing-zkrollup-websnark-bn128-two-pairings',
    'engine_name': 'v8-turbofan',
    'scoutts_cmd': 'npm run start:turbofan bn128pairing.yaml',
    'scoutts_working_dir': '/scoutyamls/scout.ts-bn128/'
  },
  {
    'bench_name': 'ecpairing-zkrollup-websnark-bn128-two-pairings',
    'engine_name': 'v8-liftoff',
    'scoutts_cmd': 'npm run start:liftoff bn128pairing.yaml',
    'scoutts_working_dir': '/scoutyamls/scout.ts-bn128/'
  },
  {
    'bench_name': 'ecpairing-zkrollup-websnark-bn128-two-pairings',
    'engine_name': 'v8-interpreter',
    'scoutts_cmd': 'node --wasm-interpret-all ./dist/cli.js bn128pairing.yaml',
    'scoutts_working_dir': '/scoutyamls/scout.ts-bn128/'
  },
  {
    'bench_name': 'daiquiri-zkmixer-websnark-bn128-groth16-four-pairings-and-mimc',
    'engine_name': 'v8-turbofan',
    'scoutts_cmd': 'npm run bench:turbofan tests/tests-withdraw.yml',
    'scoutts_working_dir': '/scoutyamls/daiquiri/'
  },
  {
    'bench_name': 'daiquiri-zkmixer-websnark-bn128-groth16-four-pairings-and-mimc',
    'engine_name': 'v8-liftoff',
    'scoutts_cmd': 'npm run bench:liftoff tests/tests-withdraw.yml',
    'scoutts_working_dir': '/scoutyamls/daiquiri/'
  },
  {
    'bench_name': 'daiquiri-zkmixer-websnark-bn128-groth16-four-pairings-and-mimc',
    'engine_name': 'v8-interpreter',
    'scoutts_cmd': 'npm run bench:interpreter tests/tests-withdraw.yml',
    'scoutts_working_dir': '/scoutyamls/daiquiri/'
  },
  {
    'bench_name': 'biturbo-token-eth1-mainnet-stateless-block-hexary-trie-keccak256-multiproof',
    'engine_name': 'v8-turbofan',
    'scoutts_cmd': 'node --no-liftoff node_modules/scout.ts/dist/cli.js turbo-token-realistic.yaml',
    'scoutts_working_dir': '/scoutyamls/biturbo/'
  },
  {
    'bench_name': 'biturbo-token-eth1-mainnet-stateless-block-hexary-trie-keccak256-multiproof',
    'engine_name': 'v8-liftoff',
    'scoutts_cmd': 'node --liftoff --no-wasm-tier-up node_modules/scout.ts/dist/cli.js turbo-token-realistic.yaml',
    'scoutts_working_dir': '/scoutyamls/biturbo/'
  },
  {
    'bench_name': 'biturbo-token-eth1-mainnet-stateless-block-hexary-trie-keccak256-multiproof',
    'engine_name': 'v8-interpreter',
    'scoutts_cmd': 'node --wasm-interpret-all node_modules/scout.ts/dist/cli.js turbo-token-realistic.yaml',
    'scoutts_working_dir': '/scoutyamls/biturbo/'
  }
]






# scout yaml files look like this:
"""
beacon_state:
  execution_scripts:
    - assembly/secp-sig-verify/out/main_with_websnark_and_keccak.wasm
shard_pre_state:
  exec_env_states:
    - "0000000000000000000000000000000000000000000000000000000000000000"
shard_blocks:
  - env: 0
    data: "d894895b62b6dc6115fe23c931f9765041a078e1241881ff8015ed312c5863d1e3ff253e8c9077c460233f62bc73d69c5364e0f2de0f7cd064173d84e53ad0bb8bbbd2f48703c59697ca33bf9077524d9df154bc944f8f6516"
shard_post_state:
  exec_env_states:
    - "00000000000000000000000029120ac3527858f5637e698cdbf0548c6b59ec77"
    #- "000000000000000000000000d683fd3465c996598dc972688b7ace676c89077b"
"""






def saveResults(benchmarks):
    result_file = os.path.join(RESULT_CSV_OUTPUT_DIR, RESULT_CSV_FILE_NAME)

    if os.path.isfile(result_file):
        print("backing up existing {}".format(result_file))
        # move existing files to old-datetime-folder
        ts = time.time()
        date_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        ts_folder_name = "{}-{}".format(date_str, round(ts))
        dest_backup_path = os.path.join(RESULT_CSV_OUTPUT_DIR, ts_folder_name)
        os.makedirs(dest_backup_path)
        shutil.move(result_file, dest_backup_path)
        print("existing csv files backed up to {}".format(dest_backup_path))

    with open(result_file, 'w', newline='') as bench_result_file:
        fieldnames = ['engine', 'bench_name', 'parse_time', 'exec_time']
        writer = csv.DictWriter(bench_result_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in benchmarks:
            writer.writerow(row)


"""
$ npm run start:turbofan secpsigverify_nobignums.yaml

> scout.ts@0.0.2 start:turbofan /Users/mbpro/dev_ewasm/scout.ts
> node --no-liftoff ./dist/cli.js "secpsigverify_nobignums.yaml"

benchmark startup took 0 seconds and 11780729 nanoseconds (11.780729ms)
benchmark execution 0 seconds and 267736023 nanoseconds (267.736023ms)
"""

def do_v8_bench(scoutts_cmd, scoutts_working_dir):
    print("running v8 benchmark...\n{}".format(scoutts_cmd))
    scoutts_cmd = shlex.split(scoutts_cmd)
    stdoutlines = []
    with subprocess.Popen(scoutts_cmd, cwd=scoutts_working_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout: # b'\n'-separated lines
            print(line, end='')
            stdoutlines.append(line)  # pass bytes as is
        p.wait()

    parse_time_regex = "benchmark startup took (\d+) seconds and \d+ nanoseconds \(([\d\w\.\s]+)\)"
    exec_time_regex = "benchmark execution took (\d+) seconds and \d+ nanoseconds \(([\d\w\.\s]+)\)"
    parse_time_line = stdoutlines[-2]
    exec_time_line = stdoutlines[-1]

    parse_time_match = re.search(parse_time_regex, parse_time_line)
    parse_time_seconds = durationpy.from_str(parse_time_match.group(1) + "s")
    parse_time_milliseconds = durationpy.from_str(parse_time_match.group(2).replace(" ", ""))
    parse_time = parse_time_seconds + parse_time_milliseconds

    exec_time_match = re.search(exec_time_regex, exec_time_line)
    exec_time_seconds = durationpy.from_str(exec_time_match.group(1) + "s")
    exec_time_milliseconds = durationpy.from_str(exec_time_match.group(2).replace(" ", ""))
    exec_time = exec_time_seconds + exec_time_milliseconds
    return { 'exec_time': exec_time.total_seconds(), 'parse_time': parse_time.total_seconds() }




"""
root@1152c9d9157f:/engines/scout.ts-bn128# /engines/scout-cpp-bn128/build/scout.exec bn128pairing_bignums.yaml
opening assembly/bn128-pairing/out/main_with_websnark_bignum_hostfuncs.wasm
called host func blockDataCopy 512016 0 576
benchmark took 0.0419916 seconds.
"""

def do_scoutcpp_bench(scoutcpp_cmd, yaml_working_dir):
    print("running scout.cpp benchmark...\n{}".format(scoutcpp_cmd))
    scoutcpp_cmd = shlex.split(scoutcpp_cmd)
    stdoutlines = []
    with subprocess.Popen(scoutcpp_cmd, cwd=yaml_working_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout: # b'\n'-separated lines
            print(line, end='')
            stdoutlines.append(line)  # pass bytes as is
        p.wait()

    timeregex = "benchmark took ([\d\.]+) seconds."
    time_line = stdoutlines[-1]
    time_match = re.search(timeregex, time_line)
    time_seconds = durationpy.from_str(time_match.group(1) + "s")
    return { 'exec_time': time_seconds.total_seconds()}





"""
/engines/wabt-bn128/out/clang/Release/wasm-interp /engines/wabt-bench-dirs/daiquiri-zkmixer-websnark-bn128-groth16-four-pairings-and-mimc-wabt-with-bignums/main_with_websnark_bignum_hostfuncs.wasm
ReadMemorySection time: 240us
eth2_savePostStateRoot: E0A30EF7356F67420D65613C3E5F718B12240227C90304CA00916B2618B5B300
parse time: 3204us
exec time: 345512us
"""

def do_wabt_bench_manual(isolated_bench_dir, wabt_cmd):
    print("running wabt_manual benchmark...\n{}".format(wabt_cmd))
    wabt_cmd = shlex.split(wabt_cmd)
    stdoutlines = []
    with subprocess.Popen(wabt_cmd, cwd=isolated_bench_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout: # b'\n'-separated lines
            print(line, end='')
            stdoutlines.append(line)  # pass bytes as is
        p.wait()

    parse_time_regex = "parse time: (\d+)us"
    exec_time_regex = "exec time: (\d+)us"
    parse_benchline = stdoutlines[-2]
    exec_benchline = stdoutlines[-1]
    parse_time_match = re.search(parse_time_regex, parse_benchline)
    parse_us_time = durationpy.from_str("{}us".format(parse_time_match.group(1)))
    exec_time_match = re.search(exec_time_regex, exec_benchline)
    exec_us_time = durationpy.from_str("{}us".format(exec_time_match.group(1)))

    return {'exec_time': exec_us_time.total_seconds(), 'parse_time': parse_us_time.total_seconds()}



"""
/engines/wabt-secp/out/clang/Release/benchmark-interp /engines/wabt-bench-dirs/ecrecover-eth1-txns-websnark-secp256k1-verify-72-sigs-wabt-with-bignums/main_with_websnark_and_keccak.wasm

ReadMemorySection time: 47us
parse succeeded..
eth2_savePostStateRoot: 00000000000000000000000029120AC3527858F5637E698CDBF0548C6B59EC77
parse time: 2685us
exec time: 883336us
execution succeeded...
register benchmark...
run benchmark...
2020-03-10 23:45:46
Running /engines/wabt-secp/out/clang/Release/benchmark-interp
Run on (1 X 2900 MHz CPU )
CPU Caches:
  L1 Data 32 KiB (x1)
  L1 Instruction 32 KiB (x1)
  L2 Unified 256 KiB (x1)
  L3 Unified 12288 KiB (x1)
Load Average: 0.39, 0.12, 0.20
eth2_savePostStateRoot: 00000000000000000000000029120AC3527858F5637E698CDBF0548C6B59EC77
------------------------------------------------------
Benchmark            Time             CPU   Iterations
------------------------------------------------------
wabt_interp     999345 us       806069 us            1
"""

def do_wabt_bench(isolated_bench_dir, wabt_cmd):
    print("\nrunning wabt benchmark...\n{}\n".format(wabt_cmd))
    wabt_cmd = shlex.split(wabt_cmd)
    stdoutlines = []
    with subprocess.Popen(wabt_cmd, cwd=isolated_bench_dir, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout: # b'\n'-separated lines
            print(line, end='')
            stdoutlines.append(line)  # pass bytes as is
        p.wait()

    parse_time_regex = "parse time: (\d+)us"
    parse_benchline = stdoutlines[3]
    parse_time_match = re.search(parse_time_regex, parse_benchline)
    parse_us_time = durationpy.from_str("{}us".format(parse_time_match.group(1)))

    exec_time_regex = "wabt_interp\s+(\d+) us"
    # maybe --benchmark_format=json is better so dont have to parse "36.775k"
    exec_benchline = stdoutlines[-1]
    exec_time_match = re.search(exec_time_regex, exec_benchline)
    exec_us_time = durationpy.from_str("{}us".format(exec_time_match.group(1)))
    return {'parse_time': parse_us_time.total_seconds(), 'exec_time': exec_us_time.total_seconds()}




def run_yaml_file_in_wabt(isolated_bench_dir, wabt_bin_path, yaml_file_dir, yaml_file_rel_path, manual=False):
    yaml_file_path = os.path.join(yaml_file_dir, yaml_file_rel_path)
    with open(yaml_file_path, 'r') as stream:
        print("running yaml file in wabt:", yaml_file_path)
        yaml_file = yaml.safe_load(stream)
        wasm_files = yaml_file['beacon_state']['execution_scripts']

        if len(wasm_files) > 1:
            print("ERROR: should only be one wasm file in the yaml file. the scout_bignum_bench.py script doesn't support more.")
            sys.exit()

        print("wasm file name:", yaml_file['beacon_state']['execution_scripts'])
        wasm_file_relative_path = wasm_files[0]

        input_data = yaml_file['shard_blocks'][0]['data']
        print("input_data size (bytes):", len(input_data)//2)

        # TODO: this test_block_data.hex is a workaround because this wabt branch doesn't support scout yaml files
        isolated_bench_path = os.path.join(WABT_BENCH_WORKING_DIR, isolated_bench_dir)
        os.makedirs(isolated_bench_path, exist_ok=True)
        isolated_input_data_path = os.path.join(isolated_bench_path, "test_block_data.hex")

        with open(isolated_input_data_path, 'w') as blockdata_file:
            blockdata_file.write(input_data)

        # copy the wasm file into isolated_bench_path
        # we assume the path in the scout yaml file is a relative path to the directory where the yaml file resides
        wasm_file_full_src_path = os.path.join(yaml_file_dir, wasm_file_relative_path)
        wasm_filename = os.path.basename(wasm_file_full_src_path)
        wasm_file_dst_path = os.path.join(isolated_bench_path, wasm_filename)
        shutil.copyfile(wasm_file_full_src_path, wasm_file_dst_path)

        # form the wabt command and execute
        #cmd_str = "./benchmark-interp {}".format(wasmfile)
        #cmd_str = "./wasm-interp {}".format(wasmfile)
        wabt_cmd = "{} {}".format(wabt_bin_path, wasm_file_dst_path)
        if manual:
            wabt_result = do_wabt_bench_manual(isolated_bench_path, wabt_cmd)
        else:
            wabt_result = do_wabt_bench(isolated_bench_path, wabt_cmd)
        return wabt_result


    print("ERROR in scout_bignum_bench.py, run_yaml_file_in_wabt()!")
    sys.exit()
    return


def main():
    scout_benchmarks = []

    # run 10 iterations of wabt_manual (ran using wabt/wasm-interp)
    for i in range(0, 10):
        print("\ndoing wabt manual bench run i=",i)
        for wabt_bench_torun in WABT_BENCH_MANUAL_INFOS:
            bench_name = wabt_bench_torun['bench_name']
            wabt_engine_name = wabt_bench_torun['engine_name']
            wabt_bin_path = wabt_bench_torun['wabt_bin_path']
            yaml_file_dir = wabt_bench_torun['yaml_file_dir']
            yaml_file_rel_path = wabt_bench_torun['yaml_file_rel_path']
            print("wabt bench: ", wabt_engine_name, bench_name)
            isolated_bench_dir = "{}-{}".format(bench_name, wabt_engine_name)
            wabt_bench_result = run_yaml_file_in_wabt(isolated_bench_dir, wabt_bin_path, yaml_file_dir, yaml_file_rel_path, manual=True)
            wabt_record = {}
            wabt_record['engine'] = wabt_engine_name
            wabt_record['bench_name'] = bench_name
            wabt_record['exec_time'] = wabt_bench_result['exec_time']
            wabt_record['parse_time'] = wabt_bench_result['parse_time']
            scout_benchmarks.append(wabt_record)
            print("got wabt_manual result:", wabt_record)

    # run only 5 iterations of wabt, since each run is an average already (ran using wabt/benchmark-interp)
    for i in range(0, 5):
        print("\ndoing wabt bench run i=",i)
        for wabt_bench_torun in WABT_BENCH_INFOS:
            bench_name = wabt_bench_torun['bench_name']
            wabt_engine_name = wabt_bench_torun['engine_name']
            wabt_bin_path = wabt_bench_torun['wabt_bin_path']
            yaml_file_dir = wabt_bench_torun['yaml_file_dir']
            yaml_file_rel_path = wabt_bench_torun['yaml_file_rel_path']
            print("wabt bench: ", wabt_engine_name, bench_name)
            isolated_bench_dir = "{}-{}".format(bench_name, wabt_engine_name)
            wabt_bench_result = run_yaml_file_in_wabt(isolated_bench_dir, wabt_bin_path, yaml_file_dir, yaml_file_rel_path, manual=False)
            wabt_record = {}
            wabt_record['engine'] = wabt_engine_name
            wabt_record['bench_name'] = bench_name
            wabt_record['exec_time'] = wabt_bench_result['exec_time']
            wabt_record['parse_time'] = wabt_bench_result['parse_time']
            scout_benchmarks.append(wabt_record)
            print("got wabt result:", wabt_record)


    # run 10 iterations of v8
    for i in range(0, 10):
        print("\ndoing v8 bench run i=",i)
        for v8_bench in V8_BENCH_INFOS:
            v8_bench_name = v8_bench['bench_name']
            v8_engine_name = v8_bench['engine_name']
            scoutts_cmd = v8_bench['scoutts_cmd']
            scoutts_working_dir = v8_bench['scoutts_working_dir']
            v8_result = do_v8_bench(scoutts_cmd, scoutts_working_dir)
            v8_record = {}
            v8_record['engine'] = v8_engine_name
            v8_record['bench_name'] = v8_bench_name
            v8_record['parse_time'] = v8_result['parse_time']
            v8_record['exec_time'] = v8_result['exec_time']
            scout_benchmarks.append(v8_record)
            print("got v8 result:", v8_record)


    # run 10 iterations of scout.cpp
    for i in range(0, 10):
        print("\ndoing scout.cpp bench run i=",i)
        for scoutcpp_bench in SCOUTCPP_BENCH_INFOS:
            scoutcpp_bench_name = scoutcpp_bench['bench_name']
            scoutcpp_engine_name = scoutcpp_bench['engine_name']
            scoutcpp_bin_path = scoutcpp_bench['scoutcpp_bin_path']
            yaml_file_path = scoutcpp_bench['yaml_file_path']
            yaml_working_dir = scoutcpp_bench['yaml_working_dir']
            scoutcpp_cmd = "{} {}".format(scoutcpp_bin_path, yaml_file_path)
            scoutcpp_result = do_scoutcpp_bench(scoutcpp_cmd, yaml_working_dir)
            scoutcpp_record = {}
            scoutcpp_record['engine'] = scoutcpp_engine_name
            scoutcpp_record['bench_name'] = scoutcpp_bench_name
            scoutcpp_record['exec_time'] = scoutcpp_result['exec_time']
            scout_benchmarks.append(scoutcpp_record)
            print("got scout.cpp result:", scoutcpp_record)


    print("got scout_benchmarks:")
    print(json.dumps(scout_benchmarks))

    saveResults(scout_benchmarks)

if __name__ == "__main__":
    main()
