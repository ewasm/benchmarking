FROM ewasm/bench-build-base:1

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1"
LABEL description="Ewasm benchmarking (geth)"

# install python modules needed for benchmarking script
RUN pip3 install durationpy jinja2 pandas

# install geth
RUN go get -u -v github.com/ewasm-benchmarking/go-ethereum
RUN cd /root/go/src/github.com/ewasm-benchmarking/go-ethereum && git checkout origin/v1.9.14-benchmarking -b v1.9.14-benchmarking && make all
RUN ln -s /root/go/src/github.com/ewasm-benchmarking/go-ethereum /go-ethereum

WORKDIR /
RUN mkdir -p /evmraceresults
RUN mkdir /evmrace

CMD /bin/bash
