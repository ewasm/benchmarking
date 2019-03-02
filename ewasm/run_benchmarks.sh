# make sure the following paths are correct for your system
REPOS_DIR=/home/user/repos/benchmarking2
TEST_DIR=$REPOS_DIR/tests
TESTETH_EXEC=$REPOS_DIR/aleth/bin/testeth
HERA_SO=$REPOS_DIR/hera/build/src/libhera.so
BENCHMARKING_DIR=$REPOS_DIR/benchmarking/ewasm


#set -x


cd $BENCHMARKING_DIR

# prepare all test case files for testeth to execute
cp $BENCHMARKING_DIR/filled/*.json $TEST_DIR/GeneralStateTests/stEWASMTests/

# the engines to use, can comment some out with #
engines=(
  binaryen
  wabt
  wavm
)

# the tests to run, can comment some out with #
tests=(
  wrc20_C
  wrc20_handwritten_faster_transfer
  wrc20_handwritten_faster_get_balance
  ed25519verify_tweetnacl
  keccak256_rhash
  sha256_nacl
  sha256_bcon
  sha256_rhash
  polynomial_evaluation_32bit
  blake2
  #bls12pairing		# need more tests
  #ecadd		# returns zeros for everything, need to check tests
  #ecmul		# returns zeros for everything, need to check tests
  #ecpairing		# very fast, something is wrong
  #ecrecover		# no test cases
  ed25519
  identity
  keccak256
  ripemd160
  sha1
  sha256
)

# create dummy lllc which may be needed by testeth
printf '#!/usr/bin/env bash\necho 1' > lllc
chmod +x lllc
PATH=$PATH:.

# double loop over each test and engine
for testcase in "${tests[@]}"; do
  #printf "\n" >> runtime_data.csv
  printf "\n\n\nBENCHMARKING %s\n" $testcase
  for engine in "${engines[@]}"; do
    printf "\n\nBENCHMARKING %s in %s\n" $testcase $engine

    # execute benchmark

    # there are two ways to get runtime data, read from stderr or read from hera_benchmarks.log
    # comment the cases in/out as you wish
    # python script takes runtimes and appends them to runtimes.txt

    ETHEREUM_TEST_PATH=$TEST_DIR $TESTETH_EXEC -t GeneralStateTests/stEWASMTests -- --vm $HERA_SO --evmc engine=$engine benchmark=true --singlenet "Byzantium" --singletest $testcase
    python3 data_collection_helpers.py hera_benchmarks.log $engine $testcase runtimes.txt
    rm hera_benchmarks.log

    #ETHEREUM_TEST_PATH=$TEST_DIR $TESTETH_EXEC -t GeneralStateTests/stEWASMTests -- --vm $HERA_SO --evmc engine=$engine benchmark=true --singlenet "Byzantium" --singletest $testcase 2> stderr.txt
    #python3 data_collection_helpers.py stderr.txt $engine $testcase runtimes.txt
    #rm stderr.txt

  done
done


