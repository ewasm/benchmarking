# Fill these in with your own system
REPOS_DIR=/home/user/repos/benchmarking2
TEST_DIR=$REPOS_DIR/tests
TESTETH_EXEC=$REPOS_DIR/aleth/bin/testeth
HERA_SO=$REPOS_DIR/hera/build/src/libhera.so
PYWEBASSEMBLY_DIR=$REPOS_DIR/pywebassembly
BINARYEN_DIR=$REPOS_DIR/binaryen
BENCHMARKING_DIR=$REPOS_DIR/benchmarking/ewasm
WASMCEPTION_DIR=$REPOS_DIR/wasmception2
EWASM_PRECOMPILES_DIR=$REPOS_DIR/ewasm-precompiles
WRC20_DIR=$REPOS_DIR/wrc20-examples


# for debugging, print out commands as they are executed, also useful to monitor
set -x


# fill dependency of testeth with dummy
cd $BENCHMARKING_DIR
# create dummy lllc which may be needed by testeth
printf '#!/usr/bin/env bash\necho 1' > lllc
chmod +x lllc
PATH=$PATH:.




#########
# WRC20 #
#########

declare -A WRC20Contracts
#if [ 1 -eq 0 ]; then
WRC20Contracts=(
  ["wrc20_C"]=footer2.txt
  ["wrc20_handwritten_faster_transfer"]=footer3.txt
  ["wrc20_handwritten_faster_get_balance"]=footer1.txt
)
#fi

cd $WRC20_DIR
git pull
cd $BENCHMARKING_DIR
cp $WRC20_DIR/C/wrc20_ewasmified.wasm wrc20_C.wasm
cp $WRC20_DIR/handwritten/wrc20_handwritten_faster_transfer.wasm .
cp $WRC20_DIR/handwritten/wrc20_handwritten_faster_get_balance.wasm .

for testcase in ${!WRC20Contracts[@]}; do
  $BINARYEN_DIR/build/bin/wasm-dis $testcase.wasm > $testcase.wat
  python3 $WRC20_DIR/tester/generate_wrc20_filler.py $testcase.wat $WRC20_DIR/tester/header.txt $WRC20_DIR/tester/${WRC20Contracts[$testcase]}
  cp ${testcase}Filler.yml $TEST_DIR/src/GeneralStateTestsFiller/stEWASMTests/
  ETHEREUM_TEST_PATH=$TEST_DIR $TESTETH_EXEC -t GeneralStateTests/stEWASMTests -- --filltests --vm $HERA_SO --evmc engine=binaryen benchmark=true --singlenet "Byzantium" --singletest $testcase
  cp $TEST_DIR/GeneralStateTests/stEWASMTests/$testcase.json $BENCHMARKING_DIR/filled/
  rm $TEST_DIR/GeneralStateTests/stEWASMTests/$testcase.json
done




#################
# C Precompiles #
#################

# C language ewasm contracts, and their test vectors, can comment some out with #
declare -A CEwasmContracts
#if [ 1 -eq 0 ]; then
CEwasmContracts=(
  ["ed25519verify_tweetnacl"]=ed25519verify.dat
  ["keccak256_rhash"]=keccak256.dat
  ["sha1_rhash"]=sha1.dat
  ["blake2b_ref"]=blake2.dat
  ["blake2b_ref_small"]=blake2.dat
  ["sha256_nacl"]=sha256.dat
  ["sha256_bcon"]=sha256.dat
  ["sha256_rhash"]=sha256.dat
  ["polynomial_evaluation_32bit"]=polynomial_evaluation_32bit.dat
)
#fi

# iterate over each C ewasm contract, compile, and generate test filler *Filler.yml, fill the json, save it, clean up
cd $BENCHMARKING_DIR
for testcase in ${!CEwasmContracts[@]}; do
  echo
  echo Benchmark $testcase
  $WASMCEPTION_DIR/dist/bin/clang --target=wasm32-unknown-unknown-wasm --sysroot=$WASMCEPTION_DIR/sysroot -O3 -g -o $testcase.wasm -nostartfiles -Wl,--allow-undefined-file=C_ewasm_contracts/c_undefined.syms,--demangle,--no-entry,--no-threads -Wl,--export=_main -fvisibility=hidden C_ewasm_contracts/$testcase.c
  $BINARYEN_DIR/build/bin/wasm-dis $testcase.wasm > $testcase.wat
  cd $PYWEBASSEMBLY_DIR/examples/
  python3 ewasmify.py $BENCHMARKING_DIR/$testcase.wasm
  cd $BENCHMARKING_DIR
  $BINARYEN_DIR/build/bin/wasm-dis ${testcase}_ewasmified.wasm > $testcase.wat
  python3 ewasm_precompile_filler_generator.py $testcase $testcase.wat test_vectors/${CEwasmContracts[$testcase]}
  cp ${testcase}Filler.yml $TEST_DIR/src/GeneralStateTestsFiller/stEWASMTests/
  ETHEREUM_TEST_PATH=$TEST_DIR $TESTETH_EXEC -t GeneralStateTests/stEWASMTests -- --filltests --vm $HERA_SO --evmc engine=binaryen --singlenet "Byzantium" --singletest $testcase
  cp $TEST_DIR/GeneralStateTests/stEWASMTests/$testcase.json $BENCHMARKING_DIR/filled/
  rm $TEST_DIR/GeneralStateTests/stEWASMTests/$testcase.json
done



####################
# Rust Precompiles #
####################

# compile Rust precompiles
cd $REPOS_DIR
#rm -rf ewasm-precompiles
#git clone https://github.com/ewasm/ewasm-precompiles
# get and compile precompiles
cd ewasm-precompiles
git pull
make
cd $BENCHMARKING_DIR
cp $EWASM_PRECOMPILES_DIR/target/wasm32-unknown-unknown/release/*.wasm .

# Rust precompiles in ewasm/ewasm-precompiles repository, along with their test vectors, can comment some out with #
declare -A RustEwasmPrecompiles
#if [ 1 -eq 0 ]; then
RustEwasmPrecompiles=(
  ["blake2"]=blake2.dat
  ["bls12pairing"]=bls12pairing.dat
  ["ecadd"]=ecadd.dat
  ["ecmul"]=ecmul.dat
  ["ecpairing"]=ecpairing.dat
  #["ecrecover"]=ecrecover.dat	# no test vectors
  ["ed25519"]=ed25519.dat
  ["identity"]=identity.dat
  ["keccak256"]=keccak256.dat
  ["ripemd160"]=ripemd160.dat
  ["sha1"]=sha1.dat
  ["sha256"]=sha256.dat
)
#fi

# iterate over each Rust Ewasm contract and generate test filler *Filler.yml
cd $BENCHMARKING_DIR
for testcase in "${!RustEwasmPrecompiles[@]}"; do
  echo
  echo Benchmark $testcase
  cp $EWASM_PRECOMPILES_DIR/target/wasm32-unknown-unknown/release/ewasm_precompile_${testcase}.wasm ${testcase}_rust.wasm
  $BINARYEN_DIR/build/bin/wasm-dis ${testcase}_rust.wasm > ${testcase}_rust.wat
  python3 ewasm_precompile_filler_generator.py ${testcase}_rust ${testcase}_rust.wat test_vectors/${RustEwasmPrecompiles[$testcase]}
  cp ${testcase}_rustFiller.yml $TEST_DIR/src/GeneralStateTestsFiller/stEWASMTests/
  ETHEREUM_TEST_PATH=$TEST_DIR $TESTETH_EXEC -t GeneralStateTests/stEWASMTests -- --filltests --vm $HERA_SO --evmc engine=binaryen --singlenet "Byzantium" --singletest ${testcase}_rust
  cp $TEST_DIR/GeneralStateTests/stEWASMTests/${testcase}_rust.json $BENCHMARKING_DIR/filled/
  rm $TEST_DIR/GeneralStateTests/stEWASMTests/${testcase}_rust.json
done




############
# clean up #
############

rm *.wasm *.wat *.yml lllc






