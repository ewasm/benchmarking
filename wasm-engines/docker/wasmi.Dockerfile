FROM ewasm/llvm-10:1.0

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1.0"
LABEL description="Ewasm benchmarking (wasmi)"

RUN git clone --single-branch --branch bench-time https://github.com/ewasm-benchmarking/wasmi.git --recursive && \
    cd wasmi && cargo test --release
