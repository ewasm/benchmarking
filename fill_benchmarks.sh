# Fill these in with your own system
REPOS_DIR=/home/user/repos/benchmarking
TEST_DIR=$REPOS_DIR/tests
TESTETH_EXEC=$REPOS_DIR/aleth/bin/testeth
HERA_SO=$REPOS_DIR/hera-benchmarking/build/src/libhera.so
PYWEBASSEMBLY_DIR=$REPOS_DIR/pywebassembly
BINARYEN_DIR=$REPOS_DIR/binaryen
BENCHMARKING_DIR=$REPOS_DIR/benchmarking
WASMCEPTION_DIR=$REPOS_DIR/wasmception
EWASM_PRECOMPILES_DIR=$REPOS_DIR/ewasm-precompiles/


# prepare stuff
cd $BENCHMARKING_DIR
# create dummy lllc which may be needed by testeth
printf '#!/usr/bin/env bash\necho 1' > lllc
chmod +x lllc
PATH=$PATH:.



###############
# C Contracts #
###############

# C language ewasm contracts, and their test vectors, can comment some out with #
declare -A CEwasmContracts
CEwasmContracts=(
  ["ed25519verify_tweetnacl"]=ed25519verify.dat
  ["keccak256_rhash"]=keccak256.dat
  ["sha256_nacl"]=sha256.dat
  ["sha256_bcon"]=sha256.dat
  ["sha256_rhash"]=sha256.dat
)

# iterate over each C ewasm contract, compile, and generate test filler *Filler.yml, fill the json, save it, clean up
cd $BENCHMARKING_DIR
for testcase in ${!CEwasmContracts[@]}; do
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
rm -rf ewasm-precompiles
git clone https://github.com/ewasm/ewasm-precompiles
# get and compile precompiles
cd ewasm-precompiles
make
cd $BENCHMARKING_DIR
cp $EWASM_PRECOMPILES_DIR/target/wasm32-unknown-unknown/release/*.wasm .

# Rust precompiles in ewasm/ewasm-precompiles repository, along with their test vectors, can comment some out with #
declare -A RustEwasmPrecompiles
RustEwasmPrecompiles=(
  ["blake2"]=blake2
  ["bls12pairing"]=bls12pairing
  ["ecadd"]=ecadd
  ["ecmul"]=ecmul
  ["ecpairing"]=ecpairing
  ["ed25519"]=ed25519
  ["identity"]=identity
  ["keccak256"]=keccak256
  ["ripemd160"]=ripemd160
  ["sha1"]=sha1
  ["sha256"]=sha256
)

# iterate over each Rust Ewasm contract and generate test filler *Filler.yml
cd $BENCHMARKING_DIR
for testcase in "${RustEwasmPrecompiles[@]}"; do
  $BINARYEN_DIR/build/bin/wasm-dis ewasm_precompile_$testcase.wasm > $testcase.wat
  python3 ewasm_precompile_filler_generator.py $testcase $testcase.wat test_vectors/${RustEwasmPrecompiles[$testcase]}
  ETHEREUM_TEST_PATH=$TEST_DIR $TESTETH_EXEC -t GeneralStateTests/stEWASMTests -- --filltests --vm $HERA_SO --evmc engine=binaryen --singlenet "Byzantium" --singletest $testcase
  cp $TEST_DIR/GeneralStateTests/stEWASMTests/$testcase.json $BENCHMARKING_DIR/filled/
  rm $TEST_DIR/GeneralStateTests/stEWASMTests/$testcase.json
done




############
# clean up #
############

rm *.wasm *.wat *.yml lllc






