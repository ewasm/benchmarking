FROM ewasm/bench-build-base:1.0

# install wagon
RUN git clone --single-branch --branch bench-times https://github.com/ewasm-benchmarking/wagon && \
    cd wagon/cmd/wasm-run && go build
