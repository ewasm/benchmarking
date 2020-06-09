FROM ewasm/bench-build-base:1.0

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1.0"
LABEL description="Ewasm benchmarking (wagon)"

# install wagon
RUN git clone --single-branch --branch bench-times https://github.com/ewasm-benchmarking/wagon && \
    cd wagon/cmd/wasm-run && go build
