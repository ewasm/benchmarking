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
$ make build_evm_engines
```

Run EVM benchmarks:

```shell
$ make benchmark_evm_engines
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
$ make build_wasm_engines
```

Build the wasm binaries and execute benchmarks:

```shell
$ cd wasm-engines && ./run_benchmarks.sh
```

### Scout Benchmarks

Build the docker image:

```shell
$ make build_scout_engines
```

Run benchmarks

```shell
make benchmark_scout_engines
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
- evmone: v0.5.0 (Jun 2020)
- geth: v1.9.14 (+ go 1.11) (May 2020)
- parity/openethereum: v2.5.1 (May 2019)

## WebAssembly engine versions

- asmble: v0.4.2-fl (+ openjdk-8-jre) (Oct 2018)
- fizzy: v0.3.0 (Jul 2020)
- life: d05763d1 (Feb 2019)
- ssvm: v0.6.0 (Jun 2020)
- v8 (node.js): v11.10.0 / v12
- wabt: 04fe0c41 (closest to v1.0.9) (Mar 2019)
- "vanilla" wabt: v1.0.17 (Jun 2020)
- wagon: v0.4.0 (Mar 2019)
- wamr: WAMR-02-18-2020 (Feb 2020)
- wasm3: v0.4.7 (Apr 2020)
- wasmi: v0.4.4 (Mar 2019)
- wasmtime: fb7c1b77 (closest to v0.31.0) (Feb 2019)
- wavm: d3607084 (closest to nightly-2019-08-28) (Aug 2019)
