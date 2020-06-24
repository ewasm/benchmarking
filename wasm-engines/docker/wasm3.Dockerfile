FROM ewasm/llvm-10:1 AS build

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1"
LABEL description="Ewasm benchmarking (wasm3)"

RUN git clone https://github.com/ewasm-benchmarking/wasm3.git --single-branch --branch v0.4.7-benchmarking && \
    cd wasm3 && mkdir build && cd build && cmake -DBUILD_WASI=none -DCMAKE_BUILD_TYPE=Release .. && make -j4

FROM ewasm/bench-build-base:1
COPY --from=build /wasm3/build/wasm3 /wasm3/build/wasm3
