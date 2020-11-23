#!/bin/bash

set -e 

# $1 = function name
# $2 = wasm file

# CWD is the directory of this script
CWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# Create input file
echo test   > testcase.inputs   # 1. Test name
echo $1    >> testcase.inputs   # 2. Function name
echo $':\n' >> testcase.inputs  # 3. Function signature
echo $'\n' >> testcase.inputs   # 4. Function parameters
echo $'\n' >> testcase.inputs   # 5. Initial Memory
echo $'\n' >> testcase.inputs   # 6. Expected result
echo $'\n' >> testcase.inputs   # 7. Expected memory

# Copy wasm file
cp $2 $CWD/testcase.wasm

$CWD/fizzy-bench --benchmark_filter=fizzy/* --benchmark_color=false $CWD | sed 's/\([0-9][0-9]*\)\s\([nm]s\)/\1\2/g'

rm -f testcase.inputs testcase.wasm
