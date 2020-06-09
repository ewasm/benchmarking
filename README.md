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

```shell
$ cd evm/geth && docker build . -t geth-bench
$ cd ../parity && docker build . -t parity-bench
$ cd ../evmone && docker build . -t evmone-bench
$ cd ../cita-vm && docker build . -t cita-vm-bench
```

Run EVM benchmarks:

```shell
$ cd evm
$ ./scripts/run_bench.sh
```

The previous command will create a new directory `evmraceresults`, containing the following files:

```
evm_benchmarks.csv         - consolidated benchmarks
evm_benchmarks_evmone.csv  - evmone benchmarks
evm_benchmarks_parity.csv  - parity benchmarks
evm_benchmarks_geth.csv    - geth benchmarks
evm_benchmarks_cita-vm.csv - cita vm benchmarks
```

Run precompiles benchmarks:

- Geth:

```shell
$ cd evm
$ ./scripts/run_precompiles_bench.py geth 
```

- Parity
```shell
$ cd evm
$ ./scripts/run_precompiles_bench.py parity
```

### Wasm Engines Benchmarks

Build the docker image:

```shell
$ cd wasm-engines
$ docker build . -t wasm-engines
```

Run the docker container:

```shell
$ cd ..
$ docker run --privileged -v $(pwd)/wasm-engines/wasmfiles:/wasmfiles -v $(pwd)/benchmark_results_data:/benchmark_results_data --security-opt seccomp=$(pwd)/wasm-engines/dockerseccompprofile.json -it wasm-engines /bin/bash
```

Build the wasm binaries and execute benchmarks:

```shell
root@docker# ./bench_wasm_and_native.sh
```

### Scout Benchmarks

Build the docker image:

```shell
$ cd scout-engines
$ docker build . -t scout-engines
```

Run the docker container:

```shell
$ cd ..
$ docker run --privileged -v $(pwd)/benchmark_results_data:/benchmark_results_data -it scout-engines /bin/bash
```

Run benchmarks

```shell
root@docker# python3 scout_bignum_bench.py
```

## Generate charts using jupyter notebooks

Install python deps for plotting benchmark graphs:

```shell
$ pip install -r requirements.txt
```

Launch a server to access generated charts in Jupyter notebooks:

```shell
$ cd notebooks
$ jupyter-notebook
```

Follow the instructions on the console to access the notebook from the browser.

Alternatively extract the images to the `images` directory by running:

```shell
$ make notebook
```

## EVM engine versions

- cita-vm: v0.1.3 (May 2019)
- evmone: 94f4e827 (closest to v0.1.0)
- geth: v1.9.14 (+ go 1.11)
- parity/openethereum: v2.5.1 (May 2019)

## WebAssembly engine versions

- asmble: v0.4.2-fl (+ openjdk-8-jre)
- fizzy: v0.1.0
- life: d05763d1
- ssvm: v0.6.0
- v8 (node.js): v11.10.0
- wabt: 04fe0c41 (closest to v1.0.9)
- wagon: e9f4420c (closest to v0.4.0)
- wamr: 130d7d07 (closest to WAMR-02-18-2020)
- wasm3: v0.4.7
- wasmi: 23b054c0 (closest to v0.4.4)
- wasmtime: fb7c1b77 (closest to v0.31.0)
- wavm: d3607084 (closest to nightly-2019-08-28)
