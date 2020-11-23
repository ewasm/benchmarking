#! /bin/bash

WASM_FILE_DIR=$1
WASM_MINIFIED_DIR=$2

echo "building wasm minifier tool"

git clone --single-branch --branch minify-tool https://github.com/ewasm/sentinel-rs.git sentinel-minify-tool
# .cargo/config sets default build target to wasm. we want to build x86 binary
# and use the command line tool, so delete .cargo/config
rm sentinel-minify-tool/.cargo/config
cd sentinel-minify-tool/wasm-utils/cli
cargo build --bin wasm-minify
# built binary sentinel-rs/wasm-utils/target/debug/wasm-minify

echo "minifying wasm files..."
rm -rf $WASM_MINIFIED_DIR
mkdir -p ${WASM_MINIFIED_DIR}

for filename in $WASM_FILE_DIR/*.wasm
do
  dest="${WASM_MINIFIED_DIR}/$(basename $filename)"
  /root/sentinel-minify-tool/wasm-utils/target/debug/wasm-minify "${filename}" "$dest"
done
