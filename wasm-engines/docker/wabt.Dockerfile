FROM ewasm/llvm-10:1 AS build

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1"
LABEL description="Ewasm benchmarking (wabt)"

RUN git clone --recursive --single-branch --branch bench-times https://github.com/ewasm-benchmarking/wabt.git && \
    mkdir wabt/build && cd wabt/build && cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTS=OFF .. && make -j4

FROM ewasm/bench-build-base:1
COPY --from=build /wabt/build/wasm-interp /wabt/build/wasm-interp
