


# WARNING: SCRIPTS ARE CURRENTLY BROKEN SINCE DEPENDENCIES ARE CHANGING. WILL REMOVE THIS WARNING WHEN EVERYTHING IS STABILIZED.


This repository contains instructions for benchmarking ewasm precompiles.

Our current method of benchmarking is built on our testing infrastructure. We use `testeth` to run a test case for each precompile, and clock its runtime. The current directory structure is as follows.

```
C_ewasm_contracts/	- contains all C contracts to be benchmarked
  c_undefined.syms	- list of ethereum helper functions, used when compiling C files
  sha256_nacl.c		- sha256 implementation from nacl library
  ...
test_vectors/		- contains allt test vectors
  sha256.dat		- list of sha256 test vectors: inputs and corresponding outputs
  ...
filled/			- contains all filled test cases, one for each precompile, ready to be benchmarked
  sha256_nacl.json	- filled test case, ready to test and benchmark
  ...
results/		- contains uploaded runtime_data.csv benchmark file from various people
  20181211_paul.txt	- the runtimes.csv from running tests
  ...
ewasm_precompile_filler_generator.py	- takes input .wat precompile and .dat file of test vectors, outputs a test filler
fill_benchmarks.sh  - for each precompile, compile it, create a test filler, and fill it
run_benchmarks.sh   - for each precompile, run it's filled test on each WebAssembly engine and and print runtimes to file
```




# Run Benchmarks

First setup tools. Do this manually step-by-step, since some user-intervention is required.

```sh
# get hera version with benchmarking enabled
git clone https://github.com/ewasm/hera.git -b benchmarking
cd hera
git submodule update --init
mkdir build && cd build
cmake -DBUILD_SHARED_LIBS=ON -DHERA_DEBUGGING=OFF -DHERA_WAVM=ON -DHERA_WABT=ON ..
# might need dependency: sudo apt-get install zlib1g-dev
make -j4
cd ../..

# get testeth
mkdir aleth
cd aleth
# visit https://github.com/ethereum/aleth/releases/ and copy the tarball url for your system (linux or darwin)
wget <tarball url> 
tar -xvzf *.tar.gz
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

This is unnecessary to run benchmarks. Use to refill benchmarks or add a new benchmark.

First setup tools.

```sh
# get hera, tests, and testeth as described above

# for C precompiles, we are currently using wasmception to compile to wasm
git clone https://github.com/yurydelendik/wasmception.git
cd wasmception
git reset --hard ef469a2bb71c73d8c25e2393fb8dd041177cf5aa	# new wasmception outputs wasm with imports like __syscall1, so use old wasmception for now
make	# Warning: this compiles llvm, llvm tools, a C library, and a C++ library. Requires lots of internet bandwidth, RAM, disk-space, and one hour compiling on a mid-level laptop.
# make note of the end of the output, should be something like --sysroot=/home/user/repos/benchmarking/wasmception/sysroot
cd ..

# for wrc20 contracts
git clone https://github.com/poemm/wrc20-examples -b C_handwritten_and_tester

# for C precompiles, we are currently using pywebassembly to clean up the wasm
git clone https://github.com/poemm/pywebassembly.git

# for Rust precompiles, get tools needed to compile
sudo apt install rustc
sudo apt install cargo
cargo install chisel
# and get precompiles
git clone https://github.com/ewasm/ewasm-precompiles.git

# binaryen is used to convert each .wasm to .wat
git clone https://github.com/WebAssembly/binaryen.git	# warning 90 MB, can also download precompiled binaries which are 15 MB
git reset --hard 8e19c94cf6c1d7609eaede0a30121bfbdc7efecc	# newer versions of binaryen cause errors, use older version for now
cd binaryen
mkdir build && cd build
cmake ..
make -j4
cd ../..
```

Compile each precompile, create test filler, fill the test, and save the filled tests.

```sh
# NOTE: edit the top of fill_benchmarks.sh to make sure the paths are correct
bash fill_benchmarks.sh
```

