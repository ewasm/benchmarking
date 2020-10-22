#! /bin/env bash

# first compile standalone wasm files from rust code, and benchmark native rust
# later, benchmark the standalone wasm files in all the wasm engines

set -e

# result output paths should be in mounted docker volumes
CSV_NATIVE_RESULTS=$BENCHMARK_RESULTS_DIR/native_benchmarks.csv
CSV_WASM_RESULTS=$BENCHMARK_RESULTS_DIR/standalone_wasm_results.csv

# benchnativerust_prepwasm.py will use rust code templates and input vectors to
# prepare standalone wasm files and native rust executables

# benchnativerust_prepwasm.py will compile rust code to wasm and save them to WASM_FILE_DIR

# files in WASM_FILE_DIR will be minified, and outputted to WASM_MINIFIED_DIR
# these files will be benchmarked in all the engines

RESULTS_DIR=$(pwd)/results #./benchmark_results_data
RUST_CODE_DIR=$(pwd)/rust-code
INPUT_VECTORS_DIR=$(pwd)/inputvectors
WASM_FILE_DIR=$RESULTS_DIR/wasmfiles
WASM_MINIFIED_DIR=$RESULTS_DIR/wasmfilesminified
RUST_BIN_DIR=$RESULTS_DIR/bin

rm -rf $RESULTS_DIR && mkdir $RESULTS_DIR
mkdir $WASM_FILE_DIR
mkdir $WASM_MINIFIED_DIR
mkdir $RUST_BIN_DIR

# save cpu info to a file, so we know what machine was used to run the benchmarks

# fill all rust benchmarks, rust test cases and compile them
docker run -v $RUST_BIN_DIR:/rust-bin -v $INPUT_VECTORS_DIR:/inputvectors -v $RESULTS_DIR:/results -v $(pwd)/rust-code:/rust-code -v $(pwd)/scripts:/scripts -it ewasm/bench-build-base:1 bash /scripts/fill_rust.sh
sudo chown -R 1000:1000 $RESULTS_DIR

echo "great success!"

# run rust benchmarks
# docker run -t ewasm/bench-build-base:1 python3.8 bench_native.py
