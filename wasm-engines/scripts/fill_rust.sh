set -e

RESULTS_DIR=/results #./benchmark_results_data
RUST_CODE_DIR=/rust-code
INPUT_VECTORS_DIR=/inputvectors
WASM_FILE_DIR=$RESULTS_DIR/wasmfiles
WASM_MINIFIED_DIR=$RESULTS_DIR/wasmfilesminified
NATIVE_DIR=$RESULTS_DIR/rustnative

cd /scripts
pip3 install -r ./requirements.txt
python3.8 fill_rust.py --wasmminifieddir $WASM_MINIFIED_DIR --wasmoutdir $WASM_FILE_DIR --rustcodedir $RUST_CODE_DIR --inputvectorsdir $INPUT_VECTORS_DIR --nativeoutdir /rust-bin
