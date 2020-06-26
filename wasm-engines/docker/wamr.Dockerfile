FROM ewasm/llvm-10:1 AS build

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1"
LABEL description="Ewasm benchmarking (wamr)"

ENV CC=/usr/bin/gcc
ENV CXX=/usr/bin/g++

RUN git clone https://github.com/ewasm-benchmarking/wasm-micro-runtime.git --single-branch --branch wamr-02-18-2020-benchmarking && \
    cd wasm-micro-runtime && \
## Build LLVM
    cd product-mini/platforms/linux && \
    ./build_llvm.sh

## Build JIT
RUN cd wasm-micro-runtime/product-mini/platforms/linux && ./build_jit.sh  && \
## Build Interpreter
    mkdir build_interp && cd build_interp && cmake -DWAMR_BUILD_INTERP=1 .. -DCMAKE_BUILD_TYPE=Release .. && make -j4 && \
## Build Compiler
    cd ../../../../wamr-compiler && mkdir build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make -j4

FROM ewasm/bench-build-base:1
COPY --from=build /wasm-micro-runtime/product-mini/platforms/linux/build_interp/iwasm /wasm-micro-runtime/product-mini/platforms/linux/build_interp/iwasm
COPY --from=build /wasm-micro-runtime/wamr-compiler/build/wamrc /wasm-micro-runtime/wamr-compiler/build/wamrc
