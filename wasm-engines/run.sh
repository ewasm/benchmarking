#! /bin/env bash

# first compile standalone wasm files from rust code, and benchmark native rust
# later, benchmark the standalone wasm files in all the wasm engines

set -e

# result output paths should be in mounted docker volumes
CSV_NATIVE_RESULTS=$BENCHMARK_RESULTS_DIR/native_benchmarks.csv
CSV_WASM_RESULTS=$BENCHMARK_RESULTS_DIR/standalone_wasm_results.csv

RESULTS_DIR=$(pwd)/results #./benchmark_results_data
RUST_CODE_DIR=$(pwd)/rust-code
INPUT_VECTORS_DIR=$(pwd)/inputvectors
WASM_FILE_DIR=$RESULTS_DIR/wasmfiles
WASM_MINIFIED_DIR=$RESULTS_DIR/wasmfilesminified
RUST_BIN_DIR=$RESULTS_DIR/rust_bin
WASM_ENGINE_BIN_DIR=$RESULTS_DIR/wasm_engine_bin

rm -rf $RESULTS_DIR && mkdir $RESULTS_DIR
mkdir $WASM_FILE_DIR
mkdir $WASM_MINIFIED_DIR
mkdir $RUST_BIN_DIR
mkdir $WASM_ENGINE_BIN_DIR

grep -E '^model name|^cpu MHz' /proc/cpuinfo > $RESULTS_DIR/cpuinfo.txt

echo "TODO some standalone wasm benchmarks are missing their source, incorporate them.  (don't delete the entire results directory on each run"

# copy all wasm engine binaries to the host machine from the container images where they were built
docker cp $(docker run -d -t ewasm/asmble:1 sleep 3s):/asmble/bin/asmble $WASM_ENGINE_BIN_DIR/asmble
docker cp $(docker run -d -t ewasm/fizzy:1 sleep 3s):/fizzy/build/bin/fizzy-bench $WASM_ENGINE_BIN_DIR/fizzy-bench
docker cp $(docker run -d -t ewasm/life:1 sleep 3s):/life/life $WASM_ENGINE_BIN_DIR/life
docker cp $(docker run -d -t ewasm/ssvm:1 sleep 3s):/SSVM/build/tools/ssvm/ssvm $WASM_ENGINE_BIN_DIR/ssvm
docker cp $(docker run -d -t ewasm/vanilla-wabt:1 sleep 3s):/vanilla-wabt/build/wasm-interp $WASM_ENGINE_BIN_DIR/vanilla-wabt
docker cp $(docker run -d -t ewasm/wabt:1 sleep 3s):/wabt/build/wasm-interp $WASM_ENGINE_BIN_DIR/wabt
docker cp $(docker run -d -t ewasm/wagon:1 sleep 3s):/wagon/cmd/wasm-run/wasm-run $WASM_ENGINE_BIN_DIR/wagon

docker cp $(docker run -d -t ewasm/wamr:1 sleep 3s):/wasm-micro-runtime/product-mini/platforms/linux/build_interp/iwasm $WASM_ENGINE_BIN_DIR/iwasm
docker cp $(docker run -d -t ewasm/wamr:1 sleep 3s):/wasm-micro-runtime/wamr-compiler/build/wamrc $WASM_ENGINE_BIN_DIR/wamrc

docker cp $(docker run -d -t ewasm/wasm3:1 sleep 3s):/wasm3/build/wasm3 $WASM_ENGINE_BIN_DIR/wasm3

docker cp $(docker run -d -t ewasm/wasmi:1 sleep 3s):/wasmi/target/release/invoke $WASM_ENGINE_BIN_DIR/invoke

docker cp $(docker run -d -t ewasm/wasmtime:1 sleep 3s):/wasmtime/target/release/wasmtime $WASM_ENGINE_BIN_DIR/wasmtime

docker cp $(docker run -d -t ewasm/wavm:1 sleep 3s):/wavm-build/bin/wavm-compile $WASM_ENGINE_BIN_DIR/wavm-compile
docker cp $(docker run -d -t ewasm/wavm:1 sleep 3s):/wavm-build/bin/wavm-run $WASM_ENGINE_BIN_DIR/wavm-run

docker run -v $RUST_BIN_DIR:/rust-bin -v $INPUT_VECTORS_DIR:/inputvectors -v $RESULTS_DIR:/results -v $(pwd)/rust-code:/rust-code -v $(pwd)/scripts:/scripts -it ewasm/bench-build-base:1 bash /scripts/fill_rust.sh

ln -s $(which node) $WASM_ENGINE_BIN_DIR/node

# copy scripts which invoke engines to wasm_bin_dir (fizzy and wamr-aot)
cp scripts/fizzy.sh $WASM_ENGINE_BIN_DIR/
cp scripts/wamr-aot.sh $WASM_ENGINE_BIN_DIR/

sudo chown -R 1000:1000 $RESULTS_DIR

echo "TODO minify rust wasm"

# run rust (native) benchmarks

python3 scripts/bench_native.py --rustbindir=$RUST_BIN_DIR --csvresults=$RESULTS_DIR

# run wasm benchmarks

python3 scripts/bench_wasm.py --wasmenginedir $WASM_ENGINE_BIN_DIR --csvfile $RESULTS_DIR/wasm_engines.csv --wasmdir $WASM_FILE_DIR

echo "TODO run rust native benchmarks"

# do stuff with the output
