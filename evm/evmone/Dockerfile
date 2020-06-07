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

# install evmone
WORKDIR /root
RUN git clone --recursive --single-branch --branch bench-evm-codes https://github.com/ewasm-benchmarking/evmone
RUN cd evmone && mkdir build
RUN cd evmone/build && cmake .. -DEVMONE_TESTING=ON
RUN cd evmone/build && cmake --build . -- -j

WORKDIR /
CMD /bin/bash

