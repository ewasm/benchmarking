FROM ewasm/llvm-10:1.0

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1.0"
LABEL description="Ewasm benchmarking (wasm3)"

RUN git clone https://github.com/ewasm-benchmarking/wasm3.git --single-branch --branch benchmark && \
    cd wasm3 && mkdir build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make -j4
