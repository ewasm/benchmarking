set -e

RESULTS_DIR=/results #./benchmark_results_data
RUST_CODE_DIR=$RESULTS_DIR/rust-code
INPUT_VECTORS_DIR=$RESULTS_DIR/inputvectors
WASM_FILE_DIR=$RESULTS_DIR/wasmfiles
WASM_MINIFIED_DIR=$RESULTS_DIR/wasmfilesminified

grep -E '^model name|^cpu MHz' /proc/cpuinfo > $RESULTS_DIR/cpuinfo.txt

cd /scripts
pip3 install -r ./requirements.txt
python3.8 fill_rust.py --wasmoutdir $WASM_FILE_DIR --rustcodedir $RUST_CODE_DIR --inputvectorsdir $INPUT_VECTORS_DIR
