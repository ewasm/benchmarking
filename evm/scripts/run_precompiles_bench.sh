#!/bin/bash

set -e

if [ "$1" == 'geth' ] || [ "$1" == 'parity' ]
then
    docker run -v $(pwd)/evmraceresults:/evmraceresults -v $(pwd)/scripts:/scripts -it $1-bench /usr/bin/python3 /scripts/bench$1precompiles.py
else
    echo Usage:
    echo "  $0 <geth|parity>"
fi
