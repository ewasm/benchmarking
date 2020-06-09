FROM ubuntu:20.04

RUN apt update -y && apt-get install -y wget && \
    wget https://github.com/ewasm-benchmarking/asmble/releases/download/0.4.2-fl-bench-times/asmble-0.4.2-fl-bench-times.tar && \
    tar -xvf asmble-0.4.2-fl-bench-times.tar
