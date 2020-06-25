#!/bin/bash

docker run --privileged \
       -v $(pwd)/benchmark_results_data:/benchmark_results_data -it ewasm/scout-engines:1 python3 scout_bignum_bench.py
