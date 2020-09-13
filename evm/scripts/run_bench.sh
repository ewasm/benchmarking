#!/bin/bash

set -e

# Run evmone benchmarks
docker run --env PYTHONIOENCODING=UTF-8 -v $(pwd)/evmraceresults:/evmraceresults -v $(pwd)/scripts:/scripts -v $(pwd)/input_data:/input_data -it ewasm/evmone-bench:1 /usr/bin/python3 /scripts/benchevm.py evmone

# Run Parity benchmarks
docker run --env PYTHONIOENCODING=UTF-8 -v $(pwd)/evmraceresults:/evmraceresults -v $(pwd)/scripts:/scripts -v $(pwd)/input_data:/input_data -it ewasm/parity-bench:1 /usr/bin/python3 /scripts/benchevm.py parity

# Run Geth benchmarks
docker run --env PYTHONIOENCODING=UTF-8 -v $(pwd)/evmraceresults:/evmraceresults -v $(pwd)/scripts:/scripts -v $(pwd)/input_data:/input_data -it ewasm/geth-bench:1 /usr/bin/python3 /scripts/benchevm.py geth

# Run cita-vm benchmarks
docker run --env PYTHONIOENCODING=UTF-8 -v $(pwd)/evmraceresults:/evmraceresults -v $(pwd)/scripts:/scripts -v $(pwd)/input_data:/input_data -it ewasm/cita-vm-bench:1 /usr/bin/python3 /scripts/benchevm.py cita-vm

# Run evmone384 benchmarks
docker run --env PYTHONIOENCODING=UTF-8 -v $(pwd)/evmraceresults:/evmraceresults -v $(pwd)/scripts:/scripts -it ewasm/evmone-evm384-bench:2 /usr/bin/python3 /scripts/bench_evm384.py

# Merge benchmarks
# TODO: just use python for merging? the docker image is only used to run python.
docker run --env PYTHONIOENCODING=UTF-8 -v $(pwd)/../benchmark_results_data:/benchmark_results_data -v $(pwd)/evmraceresults:/evmraceresults -v $(pwd)/scripts:/scripts -it ewasm/cita-vm-bench:1 /usr/bin/python3 /scripts/merge.py
