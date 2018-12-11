
This repository contains instructions for benchmarking ewasm precompiles.

Our current method of benchmarking is built on our testing infrastructure. We use `testeth` to run a test case for each precompile, and clock its runtime. The current directory structure is as follows.

```
precompiles/		- contains everything to compile all precompiles
  c_undefined.syms	- list of ethereum helper functions, used when compiling C files
  sha256.dat		- list of sha256 test vectors: inputs and corresponding outputs
  sha256_c_1.c		- a version of sha256 written in C
  sha256_c_2.c		- another version of sha256 written in C
  ...
filled/			- contains all filled test cases, one for each precompile, ready to be benchmarked
  sha256_c_1.json	- filled test case, ready to test and benchmark
  sha256_c_2.json	- filled test case, ready to test and benchmark
  ...
benchmark_results/	- contains uploaded runtime_data.csv benchmark file from various people
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
# we assume the following is done from the parent directory of this benchmarking repo

# make sure the following paths are correct for your system
REPOS_DIR=/home/user/repos/benchmarking
TEST_DIR=$REPOS_DIR/tests
TESTETH_EXEC=$REPOS_DIR/aleth/bin/testeth
HERA_SO=$REPOS_DIR/hera-benchmarking/build/src/libhera.so
BENCHMARKING_DIR=$REPOS_DIR/benchmarking

cd $BENCHMARKING_DIR

# prepare all files for testeth to execute, each file corresponds to a precompile
cp $BENCHMARKING_DIR/filled/*.json $TEST_DIR/GeneralStateTests/stEWASMTests/

# the engines to use, can comment some out with #
engines=(
  binaryen
  wabt
  wavm
)

# the tests to run, can comment some out with #
tests=(
  sha256_1
  sha256_2
)

# finally, loop over each test and engine
for testcase in "${tests[@]}"; do
  printf "\n" >> runtime_data.csv
  printf "\n\n\nBENCHMARKING %s\n" $testcase
  for engine in "${engines[@]}"; do
    printf "\n\nBENCHMARKING %s in %s\n" $testcase $engine

    # prepare file to output to
    printf "\n%s, %s\t" $testcase $engine >> runtime_data.csv
    # for wavm benchmarks, prepare to append compile and invokation times
    if [ "$engine" = "wavm" ]; then
      printf "\n%s, %s\t" $testcase wavm_compile >> runtime_data_wavm_compile.csv
      printf "\n%s, %s\t" $testcase wavm_invoke >> runtime_data_wavm_invoke.csv
    fi

    printf "\nBENCHMARKING %s in %s\n" $testcase $engine
    ETHEREUM_TEST_PATH=$TEST_DIR $TESTETH_EXEC -t GeneralStateTests/stEWASMTests -- --vm $HERA_SO --evmc engine=$engine --singlenet "Byzantium" --singletest $testcase

    # for wavm benchmarks, append compile and invokation times from other files
    if [ "$engine" = "wavm" ]; then
      printf "\n" >> runtime_data.csv
      tail runtime_data_wavm_compile.csv -n 1 >> runtime_data.csv
      rm runtime_data_wavm_compile.csv
      printf "\n" >> runtime_data.csv
      tail runtime_data_wavm_invoke.csv -n 1 >> runtime_data.csv
      rm runtime_data_wavm_invoke.csv
    fi

  done
done
```

In file `runtime_data.csv`, the extra time for each test corresponds to the ewasm contract which calls the precompile for each input and stores the output. This is the first instantiation-time and the last run-time, perhaps we will automatically delete if it becomes a problem.







# Create Benchmarks

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
# Fill these in with your own system
REPOS_DIR=/home/user/repos/benchmarking
TEST_DIR=$REPOS_DIR/tests
TESTETH_EXEC=$REPOS_DIR/aleth/bin/testeth
HERA_SO=$REPOS_DIR/hera-benchmarking/build/src/libhera.so
PYWEBASSEMBLY_DIR=$REPOS_DIR/pywebassembly
BINARYEN_DIR=$REPOS_DIR/binaryen
BENCHMARKING_DIR=$REPOS_DIR/benchmarking
WASMCEPTION_DIR=$REPOS_DIR/wasmception

# compile each precompile
cd $BENCHMARKING_DIR
$WASMCEPTION_DIR/dist/bin/clang --target=wasm32-unknown-unknown-wasm --sysroot=$WASMCEPTION_DIR/sysroot -O3 -g -o sha256_c_1.wasm -nostartfiles -Wl,--allow-undefined-file=$BENCHMARKING_DIR/precompiles/c_undefined.syms,--demangle,--no-entry,--no-threads -Wl,--export=_main -fvisibility=hidden $BENCHMARKING_DIR/precompiles/sha256_c_1.c
$WASMCEPTION_DIR/dist/bin/clang --target=wasm32-unknown-unknown-wasm --sysroot=$WASMCEPTION_DIR/sysroot -O3 -g -o sha256_c_2.wasm -nostartfiles -Wl,--allow-undefined-file=$BENCHMARKING_DIR/precompiles/c_undefined.syms,--demangle,--no-entry,--no-threads -Wl,--export=_main -fvisibility=hidden $BENCHMARKING_DIR/precompiles/sha256_c_2.c

# For C-language precompiles, use PyWebAssembly to clean them up
cd $PYWEBASSEMBLY_DIR/examples/
python3 ewasmify.py $BENCHMARKING_DIR/sha256_c_1.wasm
python3 ewasmify.py $BENCHMARKING_DIR/sha256_c_2.wasm

# use binaryen to convert each .wasm to .wat
cd $BENCHMARKING_DIR
$BINARYEN_DIR/build/bin/wasm-dis sha256_c_1_ewasmified.wasm > sha256_c_1.wat
$BINARYEN_DIR/build/bin/wasm-dis sha256_c_2_ewasmified.wasm > sha256_c_2.wat

# create a filler for each .wat precompile
cd $BENCHMARKING_DIR
python3 ewasm_precompile_filler_generator.py sha256_c_1 sha256_c_1.wat precompiles/sha256.dat
python3 ewasm_precompile_filler_generator.py sha256_c_2 sha256_c_2.wat precompiles/sha256.dat

# put fillers into the fillers directory
cp *.yml $TEST_DIR/src/GeneralStateTestsFiller/stEWASMTests/

# create dummy lllc which may be needed by testeth
printf '#!/usr/bin/env bash\necho 1' > lllc
chmod +x lllc
PATH=$PATH:.

# fill each test
ETHEREUM_TEST_PATH=$TEST_DIR $TESTETH_EXEC -t GeneralStateTests/stEWASMTests -- --filltests --vm $HERA_SO --evmc engine=binaryen --singlenet "Byzantium" --singletest sha256_c_1
ETHEREUM_TEST_PATH=$TEST_DIR $TESTETH_EXEC -t GeneralStateTests/stEWASMTests -- --filltests --vm $HERA_SO --evmc engine=binaryen --singlenet "Byzantium" --singletest sha256_c_2

# save filled tests into our repo for others to use
cp $TEST_DIR/GeneralStateTests/stEWASMTests/sha256_c_1.json $BENCHMARKING_DIR/filled/
cp $TEST_DIR/GeneralStateTests/stEWASMTests/sha256_c_2.json $BENCHMARKING_DIR/filled/

# clean up
rm *.wasm *.wat *.yml lllc
```

