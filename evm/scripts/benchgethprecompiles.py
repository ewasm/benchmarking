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

RESULT_CSV_FILENAME = "geth_precompile_benchmarks.csv"

GO_PRECOMPILE_BENCH_CMD = "go test -timeout 900s -bench BenchmarkPrecompiled -benchtime 10s"
GO_DIR = "/go-ethereum/core/vm/"


"""
$ go test -bench BenchmarkPrecompiled -benchtime 5s
goos: linux
goarch: amd64
pkg: github.com/ethereum/go-ethereum/core/vm
BenchmarkPrecompiledEcrecover/-Gas=3000-2         	   50000	    159077 ns/op
BenchmarkPrecompiledSha256/128-Gas=108-2          	10000000	       639 ns/op
BenchmarkPrecompiledRipeMD/128-Gas=1080-2         	 3000000	      2030 ns/op
BenchmarkPrecompiledIdentity/128-Gas=27-2         	500000000	        17.2 ns/op
BenchmarkPrecompiledModExp/eip_example1-Gas=13056-2         	  200000	     34735 ns/op
BenchmarkPrecompiledModExp/eip_example2-Gas=13056-2         	 1000000	      7713 ns/op
BenchmarkPrecompiledModExp/nagydani-1-square-Gas=204-2      	 3000000	      2590 ns/op
BenchmarkPrecompiledModExp/nagydani-1-qube-Gas=204-2        	 2000000	      3357 ns/op
BenchmarkPrecompiledModExp/nagydani-1-pow0x10001-Gas=3276-2 	  500000	     13991 ns/op
BenchmarkPrecompiledModExp/nagydani-2-square-Gas=665-2      	 2000000	      4215 ns/op
BenchmarkPrecompiledModExp/nagydani-2-qube-Gas=665-2        	 1000000	      6248 ns/op
BenchmarkPrecompiledModExp/nagydani-2-pow0x10001-Gas=10649-2         	  200000	     31272 ns/op
BenchmarkPrecompiledModExp/nagydani-3-square-Gas=1894-2              	 1000000	      7558 ns/op
BenchmarkPrecompiledModExp/nagydani-3-qube-Gas=1894-2                	  500000	     12706 ns/op
BenchmarkPrecompiledModExp/nagydani-3-pow0x10001-Gas=30310-2         	  100000	     78718 ns/op
BenchmarkPrecompiledModExp/nagydani-4-square-Gas=5580-2              	  500000	     18090 ns/op
BenchmarkPrecompiledModExp/nagydani-4-qube-Gas=5580-2                	  200000	     36116 ns/op
BenchmarkPrecompiledModExp/nagydani-4-pow0x10001-Gas=89292-2         	   30000	    207740 ns/op
BenchmarkPrecompiledModExp/nagydani-5-square-Gas=17868-2             	  200000	     45934 ns/op
BenchmarkPrecompiledModExp/nagydani-5-qube-Gas=17868-2               	  100000	     99434 ns/op
BenchmarkPrecompiledModExp/nagydani-5-pow0x10001-Gas=285900-2        	   10000	    659933 ns/op
BenchmarkPrecompiledBn256Add/chfast1-Gas=500-2                       	  500000	     14068 ns/op
BenchmarkPrecompiledBn256Add/chfast2-Gas=500-2                       	  500000	     14136 ns/op
BenchmarkPrecompiledBn256Add/cdetrio1-Gas=500-2                      	10000000	      1032 ns/op
BenchmarkPrecompiledBn256Add/cdetrio2-Gas=500-2                      	10000000	      1110 ns/op
BenchmarkPrecompiledBn256Add/cdetrio3-Gas=500-2                      	 5000000	      1189 ns/op
BenchmarkPrecompiledBn256Add/cdetrio4-Gas=500-2                      	10000000	      1135 ns/op
BenchmarkPrecompiledBn256Add/cdetrio5-Gas=500-2                      	10000000	      1199 ns/op
BenchmarkPrecompiledBn256Add/cdetrio6-Gas=500-2                      	 5000000	      1417 ns/op
BenchmarkPrecompiledBn256Add/cdetrio7-Gas=500-2                      	 5000000	      1495 ns/op
BenchmarkPrecompiledBn256Add/cdetrio8-Gas=500-2                      	 5000000	      1552 ns/op
BenchmarkPrecompiledBn256Add/cdetrio9-Gas=500-2                      	 5000000	      1611 ns/op
BenchmarkPrecompiledBn256Add/cdetrio10-Gas=500-2                     	 5000000	      1440 ns/op
BenchmarkPrecompiledBn256Add/cdetrio11-Gas=500-2                     	  500000	     14456 ns/op
BenchmarkPrecompiledBn256Add/cdetrio12-Gas=500-2                     	  500000	     14485 ns/op
BenchmarkPrecompiledBn256Add/cdetrio13-Gas=500-2                     	  500000	     14315 ns/op
BenchmarkPrecompiledBn256Add/cdetrio14-Gas=500-2                     	 3000000	      2164 ns/op
BenchmarkPrecompiledBn256ScalarMul/chfast1-Gas=40000-2               	  100000	     97875 ns/op
BenchmarkPrecompiledBn256ScalarMul/chfast2-Gas=40000-2               	  100000	    105280 ns/op
BenchmarkPrecompiledBn256ScalarMul/chfast3-Gas=40000-2               	  100000	    101911 ns/op
BenchmarkPrecompiledBn256ScalarMul/cdetrio1-Gas=40000-2              	  100000	    108458 ns/op
BenchmarkPrecompiledBn256ScalarMul/cdetrio6-Gas=40000-2              	  100000	    107855 ns/op
BenchmarkPrecompiledBn256ScalarMul/cdetrio11-Gas=40000-2             	  100000	    108114 ns/op
BenchmarkPrecompiledBn256Pairing/jeff1-Gas=260000-2                  	    2000	   3259099 ns/op
BenchmarkPrecompiledBn256Pairing/jeff2-Gas=260000-2                  	    2000	   3203017 ns/op
BenchmarkPrecompiledBn256Pairing/jeff3-Gas=260000-2                  	    2000	   3230769 ns/op
BenchmarkPrecompiledBn256Pairing/jeff4-Gas=340000-2                  	    2000	   4320089 ns/op
BenchmarkPrecompiledBn256Pairing/jeff5-Gas=340000-2                  	    2000	   4314707 ns/op
BenchmarkPrecompiledBn256Pairing/jeff6-Gas=260000-2                  	    2000	   3250827 ns/op
BenchmarkPrecompiledBn256Pairing/empty_data-Gas=100000-2             	   10000	   1027267 ns/op
BenchmarkPrecompiledBn256Pairing/one_point-Gas=180000-2              	    3000	   2130905 ns/op
BenchmarkPrecompiledBn256Pairing/two_point_match_2-Gas=260000-2      	    2000	   3183844 ns/op
BenchmarkPrecompiledBn256Pairing/two_point_match_3-Gas=260000-2      	    2000	   3181564 ns/op
BenchmarkPrecompiledBn256Pairing/two_point_match_4-Gas=260000-2      	    2000	   3222494 ns/op
BenchmarkPrecompiledBn256Pairing/ten_point_match_1-Gas=900000-2      	    1000	  11762181 ns/op
BenchmarkPrecompiledBn256Pairing/ten_point_match_2-Gas=900000-2      	    1000	  11861035 ns/op
BenchmarkPrecompiledBn256Pairing/ten_point_match_3-Gas=260000-2      	    2000	   3186670 ns/op
PASS
ok  	github.com/ethereum/go-ethereum/core/vm	510.099s
"""

def do_go_precompile_bench():
    go_cmd = shlex.split(GO_PRECOMPILE_BENCH_CMD)
    print("running go precompile benchmarks...\n{}".format(GO_PRECOMPILE_BENCH_CMD))

    raw_stdoutlines = []
    with subprocess.Popen(go_cmd, cwd=GO_DIR, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout: # b'\n'-separated lines
            print(line, end='')
            raw_stdoutlines.append(line)  # pass bytes as is
        p.wait()

    #stdoutlines = [line.decode('utf8') for line in raw_stdoutlines]
    # line.decode('utf8') crashes python.  AttributeError: 'str' object has no attribute 'decode'
    print("process done.  got stdout:", raw_stdoutlines)
    return raw_stdoutlines

# parsing code from https://github.com/ethereum/benchmarking/blob/master/constantinople/scripts/postprocess_geth_v2.py
def parse_go_bench_output(stdoutlines):
    benchRegex = "Benchmark(Precompiled.*)-Gas=([\d]+)\S+\s+\d+\s+([\d\.]+) ns\/op"
    #opRegexp = re.compile("Benchmark(Op.*)\S+\s+\d+\s+([\d\.]+) ns\/op") 

    bench_tests = []
    for line in stdoutlines:
        match = re.search(benchRegex, line)
        if match:
            (name, gas, nanosecs) = (match.group(1), match.group(2), match.group(3))
            bench_time = durationpy.from_str("{}ns".format(nanosecs))
            bench_tests.append({'name': name, 'gas': gas, 'time': bench_time.total_seconds()})

    return bench_tests


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
        fieldnames = ['test_name', 'gas', 'time']
        writer = csv.DictWriter(bench_result_file, fieldnames=fieldnames)
        writer.writeheader()
        for test_result in precompile_benchmarks:
            writer.writerow({"test_name" : test_result['name'], "gas" : test_result['gas'], "time" : test_result['time']})


def apply_patch_for_ecpairing_input():
    git_cmd = shlex.split("git apply /scripts/geth_ecpairing_precompile_rollup_input.patch")
    print("applying patch to add ecpairing rollup input to geth precompile benchmarks...\n{}".format(git_cmd))

    with subprocess.Popen(git_cmd, cwd="/go-ethereum/", stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, universal_newlines=True) as p:
        for line in p.stdout: # b'\n'-separated lines
            print(line, end='')
        p.wait()



def main():
    apply_patch_for_ecpairing_input()
    bench_output = do_go_precompile_bench()
    bench_results = parse_go_bench_output(bench_output)
    print("got precompile benchmarks:", bench_results)

    # TODO: bench parity precompiles

    saveResults(bench_results)


if __name__ == "__main__":
    main()
