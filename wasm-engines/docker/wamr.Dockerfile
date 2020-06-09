FROM ewasm/llvm-10:1.0

ENV CC=/usr/bin/gcc
ENV CXX=/usr/bin/g++

RUN git clone https://github.com/ewasm-benchmarking/wasm-micro-runtime.git --single-branch --branch benchmark && \
    cd wasm-micro-runtime && git pull origin benchmark && \
## Build LLVM
    cd product-mini/platforms/linux && \
    ./build_llvm.sh

## Build JIT
RUN cd wasm-micro-runtime/product-mini/platforms/linux && ./build_jit.sh  && \
## Build Interpreter
    mkdir build_interp && cd build_interp && cmake -DWAMR_BUILD_INTERP=1 .. -DCMAKE_BUILD_TYPE=Release .. && make -j4 && \
## Build Compiler
    cd ../../../../wamr-compiler && mkdir build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make
