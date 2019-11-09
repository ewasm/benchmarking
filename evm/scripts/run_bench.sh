#!/bin/bash

# Run evmone benchmarks
docker run --env PYTHONIOENCODING=UTF-8 -v $(pwd)/evmraceresults:/evmraceresults -v $(pwd)/scripts:/scripts -v $(pwd)/input_data:/input_data -it evmone-bench /usr/bin/python3 /scripts/benchevm.py evmone

# Run Parity benchmarks
docker run --env PYTHONIOENCODING=UTF-8 -v $(pwd)/evmraceresults:/evmraceresults -v $(pwd)/scripts:/scripts -v $(pwd)/input_data:/input_data -it parity-bench /usr/bin/python3 /scripts/benchevm.py parity

# Run Geth benchmarks
docker run --env PYTHONIOENCODING=UTF-8 -v $(pwd)/evmraceresults:/evmraceresults -v $(pwd)/scripts:/scripts -v $(pwd)/input_data:/input_data -it geth-bench /usr/bin/python3 /scripts/benchevm.py geth

# Run cita-vm benchmarks
docker run --env PYTHONIOENCODING=UTF-8 -v $(pwd)/evmraceresults:/evmraceresults -v $(pwd)/scripts:/scripts -v $(pwd)/input_data:/input_data -it cita-vm-bench /usr/bin/python3 /scripts/benchevm.py cita-vm

# Merge benchmarks
docker run --env PYTHONIOENCODING=UTF-8 -v $(pwd)/evmraceresults:/evmraceresults -v $(pwd)/scripts:/scripts -v $(pwd)/input_data:/input_data -it cita-vm-bench /usr/bin/python3 /scripts/merge.py

