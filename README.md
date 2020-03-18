# Benchmarks

This repository contains instructions for benchmarking evm implementations, ewasm contracts and standalone wasm modules. Directory descriptions follow.

```
evm/            - contains benchmarks for different evm implementations (geth, parity, cita-vm, evmone)
ewasm/          - contains benchmarks and tests for ewasm contracts in ewasm engines.
wasm/           - contains benchmarks for wasm modules in standalone wasm engines.
wasm-engines/   - contains benchmarks for wasm modules comparing wasm engines.
```

## EVM

Directory `/evm` contains a list of the current benchmarked evm implementations:

```
evm/
  cita-vm/
  evmone/
  geth/
  parity/
```

Build each one of the evm implementations:

```
$ cd evm/geth && docker build . -t geth-bench
$ cd ../parity && docker build . -t parity-bench
$ cd ../evmone && docker build . -t evmone-bench
$ cd ../cita-vm && docker build . -t cita-vm-bench
```

Run EVM benchmarks:

```
$ cd evm/
$ ./scripts/run_bench.sh
```

The previous command will create a new directory `evmraceresults`, containing the following files:

- evm_benchmarks.csv - consolidated benchmarks
- evm_benchmarks_evmone.csv - evmone benchmarks
- evm_benchmarks_parity.csv - parity benchmarks
- evm_benchmarks_geth.csv - geth benchmarks
- evm_benchmarks_cita-vm.csv - cita vm benchmarks

Run precompiles benchmarks:

- Geth:

```
$ cd evm/
$ ./scripts/run_precompiles_bench.py geth 
```

- Parity
```
$ cd evm/
$ ./scripts/run_precompiles_bench.py parity
```

### Wasm Engines Benchmarks

Build the docker image:

    $ cd wasm-engines
    $ docker build . -t wasm-engines
    
Run the docker container:

    $ cd ..
    $ docker run --privileged -v $(pwd)/wasm-engines/wasmfiles:/wasmfiles -v $(pwd)/benchmark_results_data:/benchmark_results_data --security-opt seccomp=$(pwd)/wasm-engines/dockerseccompprofile.json -it wasm-engines /bin/bash

Build the wasm binaries and execute benchmarks:

    root@docker# ./bench_wasm_and_native.sh
    
### Scout Benchmarks

Build the docker image:

    $ cd scout-engines
    $ docker build . -t scout-engines
    
Run the docker container:

    $ cd ..
    $ docker run --privileged -v $(pwd)/benchmark_results_data:/benchmark_results_data -it scout-engines /bin/bash

Run benchmarks

    root@docker# python3 scout_bignum_bench.py

## Generate charts using jupyter notebooks

The simplest way to install jupyter notebooks and the dependencies needed to generate the chart is by using Conda:

1. Download the miniconda installer from: https://docs.conda.io/en/latest/miniconda.html
2. Execute the installer
```
$ bash Miniconda3-latest-Linux-x86_64.sh
```
3. Follow the prompts on the installer screens
4. Install jupyterlab
```
$ conda install jupyterlab
```
5. Install other dependencies
```
$ conda install pandas
$ pip install durationpy  # Be sure you are using conda's pip
$ conda install -c phlya adjusttext
```
Once jupyter notebooks and the dependencies are installed, the charts can be generated using the following commands:

```
$ cd notebooks
$ jupyter-notebook
```
A web server will be launched with the already generated charts, where you can also execute each step.

## Generate charts using python script

Execute the python script:

    $ cd scripts
    $ python3 generate_report.py
    
