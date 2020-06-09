FROM ewasm/llvm-10:1.0

RUN git clone --single-branch --branch bench-times https://github.com/ewasm-benchmarking/wasmtime.git && \
    cd wasmtime && cargo build --release
