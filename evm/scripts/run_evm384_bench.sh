#!/bin/bash

set -e

docker run -v $(pwd)/evmraceresults:/evmraceresults -v $(pwd)/scripts:/scripts -it evmone-evm384 /usr/bin/python3 /scripts/bench_evm384.py
