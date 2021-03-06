#!/bin/bash

set -e 

# $1 = function name
# $2 = wasm file

# Create input file
echo test   > testcase.inputs   # 1. Test name
echo $1    >> testcase.inputs   # 2. Function name
echo $':\n' >> testcase.inputs  # 3. Function signature
echo $'\n' >> testcase.inputs   # 4. Function parameters
echo $'\n' >> testcase.inputs   # 5. Initial Memory
echo $'\n' >> testcase.inputs   # 6. Expected result
echo $'\n' >> testcase.inputs   # 7. Expected memory

# Copy wasm file
cp $2 ./testcase.wasm

/engines/fizzy/fizzy-bench --benchmark_filter=fizzy/* --benchmark_color=false ./ | sed 's/\([0-9][0-9]*\)\s\([nm]s\)/\1\2/g'

rm -f testcase.inputs testcase.wasm
