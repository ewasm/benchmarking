# EVM benchmarks (2019-05-23)

- [Introduction](#introduction)
- [Benchmarks](#benchmarks)
  * [sha1](#sha1)
  * [blake2b](#blake2b)
  * [bn128mul](#bn128mul)
  * [bn256mulG2](#bn256mulg2)
- [Methodology details](#methodology-details)
  * [which EVM implementations are benchmarked and how?](#which-evm-implementations-are-benchmarked-and-how)
  * [Where can I find the EVM bytecode that was benchmarked?](#where-can-i-find-the-evm-bytecode-that-was-benchmarked)
  * [What machine and OS was used to run the benchmarks?](#what-machine-and-os-was-used-to-run-the-benchmarks)
  * [More about evmone and cita-vm](#more-about-evmone-and-cita-vm)
    + [cita-vm:](#cita-vm-)
    + [evmone:](#evmone-)


# Introduction

These benchmarks were prepared by the Ewasm team. This section on EVM is an excerpt from a forthcoming benchmarking report (which is not published yet but will be soon(TM)), made available for the purpose of discussion around [EIP-2045: Particle gas costs](https://eips.ethereum.org/EIPS/eip-2045).

The results below show [evmone](https://github.com/chfast/evmone/) setting new speed records, demonstrating the performance attainable by executing EVM bytecode in an optimized interpreter.

# Benchmarks


## sha1

![](https://storage.googleapis.com/ethereum-hackmd/upload_a3cfb6571bc14a831df66cb3fbbcfd31.png)

![](https://storage.googleapis.com/ethereum-hackmd/upload_31ca2ec91be842654a1859ad12392f2e.png)

Sha1 with shift opcodes uses SHL and SHR opcodes (adopted in Constantinople).

## blake2b

![](https://storage.googleapis.com/ethereum-hackmd/upload_f5dc9a1a152b42116e79c8a4d7541787.png)

![](https://storage.googleapis.com/ethereum-hackmd/upload_5ff6f342a5a72e9b8d8e6af3bb5fb2f7.png)

Blake2b with shift opcodes uses SHL and SHR opcodes (adopted in Constantinople).

![](https://storage.googleapis.com/ethereum-hackmd/upload_7f0f5cd3bed58b34a1e331590eed593c.png)

Blake2b with [Huff](https://github.com/AztecProtocol/AZTEC/blob/feat-huff-truffle-integration-ho-ho-ho/packages/weierstrudel/huff_modules/blake2b.huff) optimizations (more info [here](https://ethereum-magicians.org/t/blake2b-f-precompile/3157/12)).

## bn128mul

![](https://storage.googleapis.com/ethereum-hackmd/upload_39dd37d59b3e018b3d4a5ba5783b2ef5.png)


The bn128mul implementation for EVM is [Weierstrudel](https://medium.com/aztec-protocol/huffing-for-crypto-with-weierstrudel-9c9568c06901), written in Huff, from AZTEC Protocol.

The `geth-precompile` and `parity-precompile` is the native Go and Rust code used for the ECMUL precompile in geth and parity (adopted in Byzantium).

Cita-evm is slower than parity-evm because the latest parity release uses a [num-bigint library](https://github.com/paritytech/parity-ethereum/pull/10600) with an optimization for 256-bit division (which is used by the `MULMOD` opcode), but cita-evm has not updated to use that library.


## bn256mulG2

![](https://storage.googleapis.com/ethereum-hackmd/upload_21aba0cddd889b4582d6f4d541bbcdfb.png)

Multiplication of Bn128/Bn256 G2 points (see [musalbas/solidity-BN256G2](https://github.com/musalbas/solidity-BN256G2) and [0xAshish/solidity-BN256G2](https://github.com/0xAshish/solidity-BN256G2)).

# Methodology details

## which EVM implementations are benchmarked and how?

Four EVM implementations are benchmarked:
1. geth - around [v1.8.25](https://github.com/ethereum/go-ethereum/releases/tag/v1.8.25) from 2019-04-12 ([this branch]() using [this benchmarking code](https://github.com/cdetrio/go-ethereum/commit/cf9cb0ec02cf29693f20e6b0f8f590912dc386a8)).
2. parity - around [beta 2.5.1](https://github.com/paritytech/parity-ethereum/releases/tag/v2.5.1) from 2019-05-14 ([this branch](https://github.com/cdetrio/parity/tree/evm-code-bencher) using [this benchmarking code](https://github.com/cdetrio/parity/blob/b06b0a30c63693759ecadb760fab5f17b33b9151/evmbin/src/main.rs#L135-L153)).
3. cita-vm - [master](https://github.com/cryptape/cita-vm) around 2019-05-20 ([this benchmarking code](https://github.com/cdetrio/cita-vm/commit/f4076919ba1b6cbda668fb6913fd2bc615627f6a)).
4. evmone - [master](https://github.com/chfast/evmone/) around 2019-04-10 ([this benchmarking code](https://github.com/chfast/evmone/pull/3)).

Benchmarking also involved some dockerfiles and python scripts, which will be better documented soon.

## Where can I find the EVM bytecode that was benchmarked?

[Here for now](https://github.com/cdetrio/benchmarking-wasm-ewasm-evm/tree/9a4786c3ec6aa212b0e2f3c5954527a1c7aa56c8/evmrace/evmcode).

## What machine and OS was used to run the benchmarks?

An Azure VM and Ubuntu 18.

```
$ cat /proc/cpuinfo | grep "model name"| head
model name      : Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz
model name      : Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz
model name      : Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz
model name      : Intel(R) Xeon(R) CPU E5-2673 v4 @ 2.30GHz
```

## More about evmone and cita-vm

### cita-vm:

Cita-vm is a rust implementation. From the [readme](https://github.com/cryptape/cita-vm/blob/master/README.md):
> Fast EVM implementation for CITA. Tuned for high performance, up to 5x faster than parity.

See other benchmarks in the [cita-vm readme](https://github.com/cryptape/cita-vm#Performance-comparison-with-parity-and-geth).

### evmone:

Evmone is a C++ implementation focused on speed.

From the [readme](https://github.com/chfast/evmone/blob/master/README.md):

> The C++ implementation of the Ethereum Virtual Machine (EVM) focused on speed. Compatible with EVMC.

> Characteristic of evmone
> 1. The "indirect" subroutine threading is the dispatch method - a table with pointers to subroutines is prepared during the analysis of the bytecode.
> 2. The gas cost and stack requirements of block of instructions is precomputed and applied once per block during execution.
> 3. The intx library is used to provide 256-bit integer precision.
> 4. The ethash library is used to provide Keccak hash function implementation needed for the special SHA3 instruction.

