#!/usr/bin/python

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

parser = argparse.ArgumentParser()
parser.add_argument('--wasmoutdir', help='full path of dir containing wasm files')
parser.add_argument('--csvresults', help='full path of csv result file')
parser.add_argument('--rustcodedir', help='comma-separated list of engines to benchmark')
parser.add_argument('--inputvectorsdir', help='comma-separated list of engines to benchmark')

args = vars(parser.parse_args())


# how many times to run native exec
RUST_BENCH_REPEATS = 50

def get_rust_bytes(hex_str):
    tmp = map(''.join, zip(*[iter(hex_str)]*2))
    tmp = map(lambda x: int(x, 16), tmp)
    tmp = map(lambda x: '{}u8'.format(x), tmp)
    tmp = reduce(lambda x, y: x+', '+y, tmp)
    return '[ '+tmp+' ]'

def bench_rust_binary(rustdir, input_name, native_exec):
    print("running rust native {}...\n{}".format(input_name, native_exec))
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
    #rustsrc = "{}/rust-code/src/bench.rs".format(os.path.abspath(benchname))
    #rustsrc = "{}/rust-code".format(os.path.abspath(benchname))
    rust_code_path = os.path.abspath(os.path.join(rust_code_dir, benchname))
    #rustsrc = "{}/rust-code".format(os.path.abspath(benchname))
    rustsrc = rust_code_path
    #rusttemplate = "{}/src/bench.rs".format(rustsrc)
    rusttemplate = os.path.join(rust_code_path, "src/bench.rs")

    if not os.path.exists(rustsrc):
        return False

    #filldir = os.path.abspath("{}/rust-code-filled".format(benchname))
    filldir = os.path.abspath(os.path.join("./rust-code-filled/", benchname))
    if os.path.exists(filldir):
        shutil.rmtree(filldir)
    shutil.copytree(rustsrc, filldir)

    template_args = {}
    for key in input.keys():
        if key == "name":
            continue
        if key == "input":
            input_len = int(len(input['input']) / 2)
            input_str = "let input: [u8; {}] = {};".format(input_len, get_rust_bytes(input['input']))
            template_args["input"] = input_str
        elif key == "expected":
            expected_len = int(len(input['expected']) / 2)
            expected_str = "let expected: [u8; {}] = {};".format(expected_len, get_rust_bytes(input['expected']))
            template_args["expected"] = expected_str
        else:
            template_args[key] = input[key]

    # fill template if necessary
    if len(template_args.keys()) > 1:
        print("filling template for {}".format(input['name']))
        with open(rusttemplate) as file_:
            template = jinja2.Template(file_.read())
            filledrust = template.render(**template_args)

        #rustfileout = "{}/src/bench.rs".format(filldir)
        rustfileout = os.path.join(filldir, "src/bench.rs")
        with open(rustfileout, 'w') as outfile:
            outfile.write(filledrust)

    # compile rust code
    benchname_rust = benchname.replace("-", "_")
    rust_native_cmd = "cargo build --release --bin {}_native".format(benchname_rust)
    print("compiling rust native {}...\n{}".format(input['name'], rust_native_cmd))
    rust_process = subprocess.Popen(rust_native_cmd, cwd=filldir, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    rust_process.wait(None)
    stdoutlines = [str(line, 'utf8') for line in rust_process.stdout]
    print(("").join(stdoutlines), end="")
    # native binary is at ./target/release/sha1_native
    exec_path = "{}/target/release/{}_native".format(filldir, benchname_rust)
    exec_size = os.path.getsize(exec_path)

    # TODO: get rustc compile time
    # TODO: also build with optimization turned off

    # TODO: run wasm through wasm-gc
    rust_wasm_cmd = "cargo build --release --lib --target wasm32-unknown-unknown"
    print("compiling rust wasm {}...\n{}".format(input['name'], rust_wasm_cmd))
    rust_process = subprocess.Popen(rust_wasm_cmd, cwd=filldir, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    rust_process.wait(None)
    stdoutlines = [str(line, 'utf8') for line in rust_process.stdout]
    print(("").join(stdoutlines), end="")
    # wasm is at ./target/wasm32-unknown-unkown/release/sha1_wasm.wasm
    wasmbin = "{}/target/wasm32-unknown-unknown/release/{}_wasm.wasm".format(filldir, benchname_rust)
    wasmdir = os.path.abspath(wasm_out_dir)
    wasmoutfile = os.path.join(wasmdir, "{}.wasm".format(input['name']))
    if not os.path.exists(wasmdir):
        os.mkdir(wasmdir)
    shutil.copy(wasmbin, wasmoutfile)

    # TODO: get cargo build compiler time and report along with exec time.

    # run rust binary
    native_times = bench_rust_binary(filldir, input['name'], "./target/release/{}_native".format(benchname_rust))
    return { 'bench_times': native_times, 'exec_size': exec_size }


def saveResults(native_benchmarks, result_file):
    #result_file = os.path.join(RESULT_CSV_OUTPUT_PATH, RESULT_CSV_FILENAME)
    # move existing files to old-datetime-folder
    ts = time.time()
    date_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    ts_folder_name = "{}-{}".format(date_str, round(ts))
    result_path = os.path.dirname(result_file)
    dest_backup_path = os.path.join(result_path, ts_folder_name)
    os.makedirs(dest_backup_path)

    #for file in glob.glob(r"{}/*.csv".format(RESULT_CSV_OUTPUT_PATH)):
    #    print("backing up existing {}".format(file))
    #    shutil.move(file, dest_backup_path)
    if os.path.isfile(result_file):
        print("backing up existing {}".format(result_file))
        shutil.move(result_file, dest_backup_path)
    print("existing csv file backed up to {}".format(dest_backup_path))

    with open(result_file, 'w', newline='') as bench_result_file:
        fieldnames = ['test_name', 'elapsed_times', 'native_file_size']
        writer = csv.DictWriter(bench_result_file, fieldnames=fieldnames)
        writer.writeheader()
        for test_name, test_results in native_benchmarks.items():
            bench_times = [str(t) for t in test_results['bench_times']]
            times_str = ", ".join(bench_times)
            writer.writerow({"test_name" : test_name, "elapsed_times" : times_str, "native_file_size" : test_results['exec_size']})


def main():
    wasm_out_dir = args['wasmoutdir']
    csv_file_path = args['csvresults']
    rust_code_dir = args['rustcodedir']
    input_vectors_dir = args['inputvectorsdir']
    rustcodes = [dI for dI in os.listdir(rust_code_dir) if os.path.isdir(os.path.join(rust_code_dir,dI))]
    #benchdirs = [dI for dI in os.listdir('./') if os.path.isdir(os.path.join('./',dI))]
    native_benchmarks = {}
    for benchname in rustcodes:
        if benchname in ["__pycache__"]:
            continue
        print("start benching: ", benchname)

        #rust_code_path = os.path.join(RUST_CODES_DIR, benchname)

        ## TODO: move input vectors to their own "standalone" folder
        # use "ewasm" folder
        inputvecs_path = os.path.join(input_vectors_dir, "{}-inputs.json".format(benchname))
        with open(inputvecs_path) as f:
            bench_inputs = json.load(f)

            for input in bench_inputs:
                print("bench input:", input['name'])
                native_input_times = do_rust_bench(benchname, input, rust_code_dir, wasm_out_dir)
                if native_input_times:
                    native_benchmarks[input['name']] = native_input_times

                print("done with input:", input['name'])

        print("done benching: ", benchname)

    print("got native_benchmarks:", native_benchmarks)
    saveResults(native_benchmarks, csv_file_path)

if __name__ == "__main__":
    main()