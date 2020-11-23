#!/bin/bash

set -e

CWD="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

$CWD/wamrc -o wasm.aot $2
$CWD/iwasm -f $1 wasm.aot
