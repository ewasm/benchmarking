FROM ubuntu:18.04

# https://github.com/kuralabs/docker-python3-dev/blob/master/Dockerfile

# System deps
RUN apt-get update \
        && apt-get install -y software-properties-common git sudo build-essential wget curl nano \
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

# Install Go 1.11
RUN add-apt-repository ppa:longsleep/golang-backports && apt-get update && apt-get install -y golang-go

# install geth
RUN go get -u -v github.com/ethereum/go-ethereum
RUN cd /root/go/src/github.com/ethereum/go-ethereum && git pull origin master && make all
RUN ln -s /root/go/src/github.com/ethereum/go-ethereum /go-ethereum

WORKDIR /
RUN mkdir -p /evmraceresults
RUN mkdir /evmrace

CMD /bin/bash

