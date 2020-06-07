#!/usr/bin/env python3

from project.WasmVMBencher import WasmVMBencher
from project.settings import vm_descriptors

import csv
import logging
import sys
import os
import time
import datetime
import shutil
import argparse

sys.stdout.reconfigure(encoding='utf-8')
# sys.stdout.reconfigure requires python 3.7
# if not using python 3.7, then you you need `PYTHONIOENCODING=UTF-8 python3 main.py`


BLACKLIST = []


parser = argparse.ArgumentParser()
parser.add_argument('--wasmdir', help='full path of dir containing wasm files')
parser.add_argument('--csvfile', help='name of csv result file')
parser.add_argument('--engines', help='comma-separated list of engines to benchmark')

args = vars(parser.parse_args())


def getTestDescriptors(wasm_dir):
    test_descriptors = {}
    for filename in os.listdir(wasm_dir):
        if filename.endswith(".wasm") and filename not in BLACKLIST:
            test_name = filename[:-5] # file name without .wasm
            test_descriptors[test_name] = os.path.join(wasm_dir, filename)
    return test_descriptors


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
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p')

    logger = logging.getLogger("wasm_bench_logger")

    wasm_dir = args['wasmdir']
    csv_file_path = args['csvfile']
    engines_to_run = args['engines']
    # "wagon,wabt,v8-liftoff,v8-turbofan,v8-interpreter,wasmtime,wavm,life-polymerase,life,wasmi,asmble"
    vms_to_run = {}
    if engines_to_run is not None:
        for engine in engines_to_run.split(","):
            vms_to_run[engine] = vm_descriptors[engine]
    else:
        # run all engines
        vms_to_run = vm_descriptors

    print("vms_to_run:", vms_to_run)
    ## TODO: print version of each engine

    vm_bencher = WasmVMBencher()
    test_descriptors = getTestDescriptors(wasm_dir)
    test_results = vm_bencher.run_tests(test_descriptors, vms_to_run)
    print("test_results:")
    print(test_results)
    save_test_results(csv_file_path, test_results)


if __name__ == '__main__':
    main()
