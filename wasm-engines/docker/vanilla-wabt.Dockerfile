FROM ewasm/llvm-10:1 AS build

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1"
LABEL description="Ewasm benchmarking (vanilla-wabt)"

RUN git clone --recursive --single-branch --branch v1.0.17-benchmarking https://github.com/ewasm-benchmarking/wabt.git vanilla-wabt && \
    mkdir vanilla-wabt/build && cd vanilla-wabt/build && cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTS=OFF .. && make -j4

FROM ewasm/bench-build-base:1
COPY --from=build /vanilla-wabt/build/wasm-interp /vanilla-wabt/build/wasm-interp
