#!/bin/bash

/engines/wasm-micro-runtime/wamr-compiler/build/wamrc -o wasm.aot $2
/engines/wasm-micro-runtime/product-mini/platforms/linux/build_interp/iwasm -f $1 wasm.aot 
