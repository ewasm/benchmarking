FROM ewasm/llvm-10:1

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1"
LABEL description="Ewasm benchmarking (wasmtime)"

RUN git clone --single-branch --branch bench-times https://github.com/ewasm-benchmarking/wasmtime.git && \
    cd wasmtime && cargo build --release
