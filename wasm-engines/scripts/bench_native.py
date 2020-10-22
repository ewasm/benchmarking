import jinja2, json, re
from functools import reduce
import subprocess
import nanodurationpy as durationpy
import csv
import time
import datetime
import os
import shutil
import glob
import argparse
import sys

# how many times to run native exec
RUST_BENCH_REPEATS = 50

def bench_rust_binary(native_exec):
    bench_times = []
    for i in range(1,RUST_BENCH_REPEATS):
        rust_process = subprocess.Popen(native_exec, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
        rust_process.wait(None)
        stdoutlines = [str(line, 'utf8') for line in rust_process.stdout]
        print(("").join(stdoutlines), end="")
        elapsedline = stdoutlines[0]
        elapsedmatch = re.search("Time elapsed in bench\(\) is: ([\w\.]+)", elapsedline)
        elapsed_time = durationpy.from_str(elapsedmatch[1])
        bench_times.append(elapsed_time.total_seconds())
    return bench_times

def write_output_to_csv(native_benchmarks, result_file):
    # TODO backup old results

    print("TODO: reincorporate native_file_size column for native_benchmarks csv output if it is actually used anywhere")

    with open(result_file, 'w', newline='') as bench_result_file:
        fieldnames = ['test_name', 'elapsed_times', 'native_file_size']
        writer = csv.DictWriter(bench_result_file, fieldnames=fieldnames)
        writer.writeheader()
        for item in native_benchmarks:
            times_str = item['elapsed_times']
            test_name = item['test_name']
            writer.writerow({"test_name" : test_name, "elapsed_times" : times_str})

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rustbindir', help='directory containing executables for standalone benchmarks compiled from rust')
    parser.add_argument('--csvresults', help='full path of csv result file')
    args = vars(parser.parse_args())

    rust_native_dir = os.path.join(os.getcwd(), 'results/bin')
    # logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(message)s',
    #                 datefmt='%m/%d/%Y %I:%M:%S %p')

    # logger = logging.getLogger("wasm_bench_logger")

    executables = glob.glob(args['rustbindir'] + "/*")

    results = []

    for binary in executables:
        result_times = bench_rust_binary(binary)
        result_times = ",".join(list(map(lambda x: str(x), result_times)))
        results.append({"test_name": os.path.basename(binary).strip("_native"), "elapsed_times": result_times})

    import pdb; pdb.set_trace()
    write_output_to_csv(results, os.path.join(args['csvresults'], "native_benchmarks.csv"))

if __name__ == "__main__":
    main()
