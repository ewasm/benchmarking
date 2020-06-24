FROM ewasm/bench-build-base:1 AS build

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1"
LABEL description="Ewasm benchmarking (wasmi)"

RUN git clone --single-branch --branch v0.4.4-benchmarking https://github.com/ewasm-benchmarking/wasmi.git --recursive && \
    cd wasmi && cargo build --release

FROM ewasm/bench-build-base:1
COPY --from=build /wasmi/target/release/invoke /wasmi/target/release/invoke
