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

def bench_rust_binary(dir, executable):
    bench_times = []
    for i in range(1,RUST_BENCH_REPEATS):
        rust_process = subprocess.Popen(native_exec, cwd=rustdir, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
        rust_process.wait(None)
        stdoutlines = [str(line, 'utf8') for line in rust_process.stdout]
        print(("").join(stdoutlines), end="")
        elapsedline = stdoutlines[0]
        elapsedmatch = re.search("Time elapsed in bench\(\) is: ([\w\.]+)", elapsedline)
        elapsed_time = durationpy.from_str(elapsedmatch[1])
        bench_times.append(elapsed_time.total_seconds())
    return bench_times

def do_rust_bench(benchname, input, rust_code_dir, wasm_out_dir):
    native_times = bench_rust_binary(filldir, input['name'], "./target/release/{}_native".format(benchname_rust))
    return { 'bench_times': native_times, 'exec_size': exec_size }

def save_test_results(result_file, results):
    # move existing files to old-datetime-folder
    print(">>> result_file:")
    print(result_file)
    if os.path.isfile(result_file):
        print("backing up existing {}".format(result_file))
        ts = time.time()
        date_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        ts_folder_name = "{}-{}".format(date_str, round(ts))
        out_dir = os.path.dirname(result_file)
        dest_backup_path = os.path.join(out_dir, ts_folder_name)
        os.makedirs(dest_backup_path)
        shutil.move(result_file, dest_backup_path)
        print("existing csv files backed up to {}".format(dest_backup_path))

    # write header
    with open(result_file, 'w', newline='') as bench_result_file:
        fieldnames = ['engine', 'test_name', 'elapsed_time', 'compile_time', 'exec_time']
        writer = csv.DictWriter(bench_result_file, fieldnames=fieldnames)
        writer.writeheader()

    # append results for each vm
    with open(result_file, 'a', newline='') as bench_result_file:
        fieldnames = ['engine', 'test_name', 'elapsed_time', 'compile_time', 'exec_time']
        writer = csv.DictWriter(bench_result_file, fieldnames=fieldnames)
        for vm in results:
            for test_name, result_records in results[vm].items():
                for record in result_records:
                    writer.writerow({"engine": vm, "test_name" : test_name, "elapsed_time" : record.time, "compile_time" : record.compile_time, "exec_time" : record.exec_time})

def main():
    rust_native_dir = os.path.join(os.getcwd(), 'results/bin')
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

    logger = logging.getLogger("wasm_bench_logger")
    vms_to_run = {}

    if engines_to_run is not None:
        for engine in engines_to_run.split(","):
            vms_to_run[engine] = vm_descriptors[engine]
    else:
        # run all engines
        vms_to_run = vm_descriptors
    
    # get the benchname as exec_file_name = {bench_name}_native
    vm_bencher = WasmVMBencher()
    test_descriptors = getTestDescriptors(wasm_dir)
    test_results = vm_bencher.run_tests(test_descriptors, rust_native_dir, vms_to_run)
    save_test_results(csv_file_path, test_results)

    pass

if __name__ == "__main__":
    main()
