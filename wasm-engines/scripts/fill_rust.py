#!/usr/bin/env python3

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

def get_rust_bytes(hex_str):
    tmp = map(''.join, zip(*[iter(hex_str)]*2))
    tmp = map(lambda x: int(x, 16), tmp)
    tmp = map(lambda x: '{}u8'.format(x), tmp)
    tmp = reduce(lambda x, y: x+', '+y, tmp)
    return '[ '+tmp+' ]'

def fill_rust(benchname, input, rust_code_dir, wasm_out_dir, native_out_dir):
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
    rust_native_cmd = "cargo build --release -j4 --bin {}_native".format(benchname_rust)
    print("compiling rust native {}...\n{}".format(input['name'], rust_native_cmd))
    rust_process = subprocess.Popen(rust_native_cmd, cwd=filldir, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    return_code = rust_process.wait(None)
    stdoutlines = [str(line, 'utf8') for line in rust_process.stdout]
    print(("").join(stdoutlines), end="")

    if return_code != 0:
        sys.exit(-1)

    # native binary is at ./target/release/sha1_native
    exec_path = "{}/target/release/{}_native".format(filldir, benchname_rust)
    exec_size = os.path.getsize(exec_path)

    # TODO: get rustc compile time
    # TODO: also build with optimization turned off

    # TODO: run wasm through wasm-gc
    rust_wasm_cmd = "cargo build --release -j4 --lib --target wasm32-unknown-unknown"
    print("compiling rust wasm {}...\n{}".format(input['name'], rust_wasm_cmd))
    rust_process = subprocess.Popen(rust_wasm_cmd, cwd=filldir, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    return_code = rust_process.wait(None)
    stdoutlines = [str(line, 'utf8') for line in rust_process.stdout]
    print(("").join(stdoutlines), end="")
    if return_code != 0:
        sys.exit(-1)
    # wasm is at ./target/wasm32-unknown-unkown/release/sha1_wasm.wasm
    exec_out_path=os.path.join(native_out_dir, input['name'])

    wasmbin = "{}/target/wasm32-unknown-unknown/release/{}_wasm.wasm".format(filldir, benchname_rust)
    wasmdir = os.path.abspath(wasm_out_dir)
    wasmoutfile = os.path.join(wasmdir, "{}.wasm".format(input['name']))
    if not os.path.exists(wasmdir):
        os.mkdir(wasmdir)

    shutil.copy(wasmbin, wasmoutfile)
    shutil.copy(exec_path, native_out_dir+"/"+input['name']+'_native')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--wasmoutdir', help='full path of dir containing wasm files')
    parser.add_argument('--rustcodedir', help='comma-separated list of engines to benchmark')
    parser.add_argument('--inputvectorsdir', help='comma-separated list of engines to benchmark')
    parser.add_argument('--nativeoutdir', help='directory to put binaries compiled from rust code')

    args = vars(parser.parse_args())

    wasm_out_dir = args['wasmoutdir']
    native_out_dir = args['nativeoutdir']
    rust_code_dir = args['rustcodedir']
    input_vectors_dir = args['inputvectorsdir']

    import pdb; pdb.set_trace()

    rustcodes = [dI for dI in os.listdir(rust_code_dir) if os.path.isdir(os.path.join(rust_code_dir,dI))]
    #benchdirs = [dI for dI in os.listdir('./') if os.path.isdir(os.path.join('./',dI))]
    native_benchmarks = {}
    for benchname in rustcodes:
        if benchname in ["__pycache__", ".cargo"]:
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
                native_input_times = fill_rust(benchname, input, rust_code_dir, wasm_out_dir, native_out_dir)

if __name__ == "__main__":
    main()
