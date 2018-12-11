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

# create dummy lllc which may be needed by testeth
printf '#!/usr/bin/env bash\necho 1' > lllc
chmod +x lllc
PATH=$PATH:.

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
