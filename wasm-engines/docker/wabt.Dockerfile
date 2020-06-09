FROM ewasm/llvm-10:1.0

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1.0"
LABEL description="Ewasm benchmarking (wabt)"

RUN git clone --recursive --single-branch --branch bench-times https://github.com/ewasm-benchmarking/wabt.git && \
    mkdir wabt/build && cd wabt/build && cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTS=OFF .. && make
