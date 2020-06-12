FROM ubuntu:18.04

# https://github.com/kuralabs/docker-python3-dev/blob/master/Dockerfile

# System deps
RUN apt-get update
RUN apt-get install -y software-properties-common git sudo build-essential wget curl nano \
    autoconf automake cmake libtool make unzip zlib1g-dev texinfo \
    gcc musl-dev

# Install Python stack
RUN apt-get update \
    && apt-get --yes --no-install-recommends install \
        python3 python3-dev \
        python3-pip python3-venv python3-wheel python3-setuptools \
        build-essential \
        python-dev \
        graphviz git openssh-client \
    && rm -rf /var/lib/apt/lists/*

# install python modules needed for benchmarking script
RUN pip3 install durationpy jinja2 pandas

WORKDIR /

# install rust
RUN curl https://sh.rustup.rs -sSf | \
    sh -s -- --default-toolchain stable -y && . $HOME/.cargo/env
ENV PATH=/root/.cargo/bin:$PATH
RUN rustup default nightly-2019-01-15

RUN rustup target add wasm32-unknown-unknown

# install parity-evm
RUN git clone --recursive --single-branch --branch v2.5.1-benchmarking https://github.com/ewasm-benchmarking/openethereum parity
RUN cd parity/evmbin && cargo build --release

# deps required to build full parity for native precompile benchmarks
RUN apt-get update
RUN apt-get install -y libudev-dev

CMD /bin/bash
