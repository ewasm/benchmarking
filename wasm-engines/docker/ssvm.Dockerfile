FROM ewasm/llvm-10:1 AS build

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1"
LABEL description="Ewasm benchmarking (ssvm)"

RUN apt update -y && apt install -y libboost-all-dev && git clone https://github.com/ewasm-benchmarking/SSVM.git --single-branch --branch v0.6.0-benchmarking && \
    cd SSVM && mkdir -p build && cd build && cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTS=OFF -DSSVM_DISABLE_AOT_RUNTIME=ON .. && make -j4

FROM ewasm/bench-build-base:1
COPY --from=build /SSVM/build/tools/ssvm/ssvm /SSVM/build/tools/ssvm/ssvm
