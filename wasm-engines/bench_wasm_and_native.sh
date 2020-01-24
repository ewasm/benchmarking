#!/usr/bin/env bash

# first compile standalone wasm files from rust code, and benchmark native rust
# later, benchmark the standalone wasm files in all the wasm engines


# result output paths should be in mounted docker volumes
CSV_NATIVE_RESULTS=/testresults/native_benchmarks.csv
CSV_WASM_RESULTS=/testresults/standalone_wasm_results.csv

# benchnativerust_prepwasm.py will use rust code templates and input vectors to
# prepare standalone wasm files and native rust executables
RUST_CODE_DIR=./rust-code
INPUT_VECTORS_DIR=./inputvectors

# benchnativerust_prepwasm.py will compile rust code to wasm and save them to WASM_FILE_DIR
WASM_FILE_DIR=/wasmfiles

# files in WASM_FILE_DIR will be minified, and outputted to WASM_MINIFIED_DIR
# these files will be benchmarked in all the engines
WASM_MINIFIED_DIR=/wasmfilesminified


# fill rust code templates with input vectors. compile rust code to wasm and native. benchmark native
# wasm will be further processed and benchmarked later
cd /benchprep
python3.7 benchnativerust_prepwasm.py --wasmoutdir="${WASM_FILE_DIR}" --csvresults="${CSV_NATIVE_RESULTS}" --rustcodedir="${RUST_CODE_DIR}" --inputvectorsdir="${INPUT_VECTORS_DIR}" |& tee prep-wasm-bench-native-run1.log



# furthur process wasm files by minifying them.

echo "building sentinel-rs branch minify-tool..."
# TODO: when wasm-chisel is ready, use it instead of sentinel-minify-tool
cd /root
rm -rf sentinel-minify-tool # delete old dir in case we are rerunning the script
git clone --single-branch --branch minify-tool https://github.com/ewasm/sentinel-rs.git sentinel-minify-tool
# .cargo/config sets default build target to wasm. we want to build x86 binary
# and use the command line tool, so delete .cargo/config
rm sentinel-minify-tool/.cargo/config
cd sentinel-minify-tool/wasm-utils/cli
cargo build --bin wasm-minify
# built binary sentinel-rs/wasm-utils/target/debug/wasm-minify

echo "minifying wasm files..."
mkdir -p ${WASM_MINIFIED_DIR}
cd "${WASM_FILE_DIR}"
for filename in *.wasm
do
  dest="${WASM_MINIFIED_DIR}/${filename}"
  /root/sentinel-minify-tool/wasm-utils/target/debug/wasm-minify "${filename}" "$dest"
done



# benchmark standalone wasm files in all the engines

cd /benchrunner
python3.7 main.py --wasmdir="${WASM_MINIFIED_DIR}" --csvfile="${CSV_WASM_RESULTS}" |& tee wasm-engines-run1.log
