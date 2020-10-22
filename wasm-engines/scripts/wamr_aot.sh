#!/bin/bash

set -e

/engines/wamr/wamrc -o wasm.aot $2
/engines/wamr/iwasm -f $1 wasm.aot 
