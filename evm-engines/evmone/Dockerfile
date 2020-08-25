FROM ewasm/bench-build-base:1

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1"
LABEL description="Ewasm benchmarking (evmone)"

RUN pip3 install durationpy jinja2 pandas

# install evmone
WORKDIR /root
RUN git clone --recursive --single-branch --branch v0.5.0 https://github.com/ethereum/evmone
RUN cd evmone && mkdir build
RUN cd evmone/build && cmake .. -DEVMONE_TESTING=ON
RUN cd evmone/build && make -j4

WORKDIR /
CMD /bin/bash
