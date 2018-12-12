
This repository contains instructions for benchmarking ewasm precompiles.

Our current method of benchmarking is built on our testing infrastructure. We use `testeth` to run a test case for each precompile, and clock its runtime. The current directory structure is as follows.

```
source/			- contains everything to compile all precompiles
  c_undefined.syms	- list of ethereum helper functions, used when compiling C files
  sha256.dat		- list of sha256 test vectors: inputs and corresponding outputs
  sha256_c_1.c		- a version of sha256 written in C
  sha256_c_2.c		- another version of sha256 written in C
  ...
filled/			- contains all filled test cases, one for each precompile, ready to be benchmarked
  sha256_c_1.json	- filled test case, ready to test and benchmark
  sha256_c_2.json	- filled test case, ready to test and benchmark
  ...
results/		- contains uploaded runtime_data.csv benchmark file from various people
  20181211_paul.txt	- the runtimes.csv from running tests
  ...
ewasm_precompile_filler_generator.py	- takes input .wat precompile and .dat file of test vectors, outputs a test filler
```




# Run Benchmarks

First, setup tools.

```sh
# get hera version with benchmarking enabled
git clone https://github.com/ewasm/hera.git hera-benchmarking	#TODO: this does not include benchmarking yet
cd hera-benchmarking
git submodule update --init
mkdir build && cd build
cmake -DBUILD_SHARED_LIBS=ON -DHERA_WAVM=ON -DHERA_WABT=ON ..
# might need dependency: sudo apt-get install zlib1g-dev
make -j4
cd ../..

# get testeth
mkdir aleth
cd aleth
wget https://github.com/ethereum/aleth/releases/download/v1.5.0-alpha.7/aleth-1.5.0-alpha.7-linux-x86_64.tar.gz
tar -xvzf aleth-1.5.0-alpha.7-linux-x86_64.tar.gz
cd ..

# get ewasm tests, testeth operates on this repo, we will copy test cases into here for benchmarking
git clone https://github.com/ewasm/tests.git	# warning: over 100 MB

# create dummy lllc which may be needed by testeth
printf '#!/usr/bin/env bash\necho 1' > lllc
chmod +x lllc
PATH=$PATH:.

# and, of course, this repo
git clone https://github.com/ewasm/benchmarking.git
```

Run the benchmarks. This will call testeth on each test, and print runtimes to file `runtime_data.csv`.

```sh
# NOTE: edit the top of run_benchmarks.sh to make sure the paths are correct
bash run_benchmarks.sh
```

In file `runtime_data.csv`, the extra time for each test corresponds to the ewasm contract which calls the precompile for each input and stores the output. This is the first instantiation-time and the last run-time, perhaps we will automatically delete if it becomes a problem.







# Fill Benchmarks

This is unnecessary to run benchmarks. But to recreate benchmarks.

Setup tools.

```sh
# get hera, tests, and testeth as described above

# for C precompiles, we are currently using wasmception to compile to wasm
git clone https://github.com/yurydelendik/wasmception.git
cd wasmception
make	# Warning: this compiles llvm, llvm tools, a C library, and a C++ library. Requires lots of internet bandwidth, RAM, disk-space, and one hour compiling on a mid-level laptop.
# make note of the end of the output, should be something like --sysroot=/home/user/repos/benchmarking/wasmception/sysroot

# for C precompiles, we are currently using pywebassembly to clean up the wasm
cd ..
git clone https://github.com/poemm/pywebassembly.git

# binaryen is used to convert each .wasm to .wat
git clone https://github.com/WebAssembly/binaryen.git	# warning 90 MB, can also download precompiled binaries which are 15 MB
cd binaryen
mkdir build && cd build
cmake ..
make -j4
```

Compile each precompile and prepare benchmark file for each precompile.

```sh
# NOTE: edit the top of fill_benchmarks.sh to make sure the paths are correct
bash fill_benchmarks.sh
```

