FROM ewasm/bench-build-base:1

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1"
LABEL description="Ewasm benchmarking (parity)"

# deps required to build full parity for native precompile benchmarks
RUN apt-get update && \
        apt-get install -y libudev-dev

# install python modules needed for benchmarking script
RUN pip3 install durationpy jinja2 pandas

RUN rustup default nightly-2019-01-15

WORKDIR /

# install parity-evm
RUN git clone --recursive --single-branch --branch v2.5.1-benchmarking https://github.com/ewasm-benchmarking/openethereum parity
RUN cd parity/evmbin && cargo build --release

CMD /bin/bash
