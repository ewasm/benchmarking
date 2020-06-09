FROM ubuntu:20.04

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1.0"
LABEL description="Build environment for Ewasm benchmarking (base image)"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get clean && \
    apt-get update && \
    apt-get install -y cmake software-properties-common git sudo build-essential wget curl nano python2.7 \
    autoconf automake libtool llvm-6.0 make ninja-build unzip zlib1g-dev texinfo libssl-dev golang python3.8 python3-distutils python3-pip && \
    curl https://sh.rustup.rs -sSf | sh -s -- --default-toolchain 1.42.0 -y && . $HOME/.cargo/env

RUN export GO111MODULE=on

ENV PATH=/root/.cargo/bin:$PATH
