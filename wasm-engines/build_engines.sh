#! /usr/bin/env bash

set -e

repo="ewasm"

# build base images
docker build -t $repo/bench-build-base:1.0 -f docker/bench-build-base.Dockerfile .
docker build -t $repo/llvm-10:1.0 -f docker/llvm-10.Dockerfile .

# build engines
docker build -t $repo/fizzy:1.0 -f docker/fizzy.Dockerfile .
docker build -t $repo/life:1.0  -f docker/life.Dockerfile .
docker build -t $repo/ssvm:1.0 -f  docker/ssvm.Dockerfile .
docker build -t $repo/wabt:1.0 -f docker/wabt.Dockerfile .
docker build -t $repo/wagon:1.0 -f docker/wagon.Dockerfile .
docker build -t $repo/wamr:1.0 -f docker/wamr.Dockerfile .
docker build -t $repo/wasm3:1.0 -f docker/wasm3.Dockerfile .
docker build -t $repo/wasmi:1.0 -f docker/wasmi.Dockerfile .
docker build -t $repo/wasmtime:1.0 -f docker/wasmtime.Dockerfile .
docker build -t $repo/wavm:1.0 -f docker/wavm.Dockerfile .
docker build -t $repo/asmble:1.0 -f docker/asmble.Dockerfile .

docker build -t $repo/bench:1.0 -f docker/bench.Dockerfile .
