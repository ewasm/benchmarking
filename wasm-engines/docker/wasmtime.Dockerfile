FROM ewasm/llvm-10:1 AS build

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1"
LABEL description="Ewasm benchmarking (wasmtime)"

RUN git clone --single-branch --branch bench-times https://github.com/ewasm-benchmarking/wasmtime.git && \
    cd wasmtime && cargo build --release

FROM ewasm/bench-build-base:1
COPY --from=build /wasmtime/target/release/wasmtime /wasmtime/target/release/wasmtime
