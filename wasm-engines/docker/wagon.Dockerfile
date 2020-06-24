FROM ewasm/bench-build-base:1 AS build

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1"
LABEL description="Ewasm benchmarking (wagon)"

# install wagon
RUN git clone --single-branch --branch v0.4.0-benchmarking https://github.com/ewasm-benchmarking/wagon && \
    cd wagon/cmd/wasm-run && go build

FROM ewasm/bench-build-base:1
COPY --from=build /wagon/cmd/wasm-run/wasm-run /wagon/cmd/wasm-run/wasm-run
