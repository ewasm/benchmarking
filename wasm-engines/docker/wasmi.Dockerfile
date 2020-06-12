FROM ewasm/llvm-10:1 as build

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1"
LABEL description="Ewasm benchmarking (wasmi)"

RUN git clone --single-branch --branch bench-time https://github.com/ewasm-benchmarking/wasmi.git --recursive && \
    cd wasmi && cargo test --release

FROM ewasm/bench-build-base:1
COPY --from=build /wasmi/target/release/examples/invoke /wasmi/target/release/examples/invoke
