#!/bin/bash

docker run --privileged \
       -v $(pwd)/benchmark_results_data:/benchmark_results_data \
       -v $(pwd)/nanodurationpy.py:/benchscript/nanodurationpy.py \
       -v $(pwd)/scout_bignum_bench.py:/benchscript/scout_bignum_bench.py \
       -it ewasm/scout-engines:1 python3 scout_bignum_bench.py
