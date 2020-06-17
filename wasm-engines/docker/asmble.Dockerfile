FROM ubuntu:20.04 AS build

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1"
LABEL description="Ewasm benchmarking (asmble)"

RUN apt update -y && apt-get install -y wget && \
    wget https://github.com/ewasm-benchmarking/asmble/releases/download/0.4.2-fl-bench-times/asmble-0.4.2-fl-bench-times.tar && \
    tar -xvf asmble-0.4.2-fl-bench-times.tar

FROM ewasm/bench-build-base:1
COPY --from=build /asmble /asmble
