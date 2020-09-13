FROM ewasm/bench-build-base:1

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1"
LABEL description="Ewasm benchmarking (evmone-evm384)"

RUN pip3 install durationpy pandas

# install evmone (need CXXFLAGS=-w or the build fails)
WORKDIR /root

# fetch evm384 binaries for different variants
RUN git clone --single-branch --branch v6 https://github.com/ewasm/evm384_f6m_mul.git

# clone and build evmone branches

# v1
RUN git clone --recursive --single-branch --branch v0.5.0-evm384-v1 https://github.com/ethereum/evmone.git evmone-evm384-v1
RUN cd evmone-evm384-v1 && mkdir build && \
  cd build && CXXFLAGS="-w" cmake .. -DEVMONE_TESTING=ON && make -j4

# v2 - v1 with `out` parameter added
RUN git clone --recursive --single-branch https://github.com/ethereum/evmone -b v0.5.0-evm384-v2 evmone-evm384-v2
RUN cd evmone-evm384-v2 && mkdir build && \
  cd build && CXXFLAGS="-w" cmake .. -DEVMONE_TESTING=ON && make -j4

# v3 - v2 with memory checks disabled for arguments in evm384 opcodes
RUN git clone --recursive --single-branch https://github.com/ethereum/evmone -b v0.5.0-evm384-v2-unsafe evmone-evm384-v3
RUN cd evmone-evm384-v3 && mkdir build && \
  cd build && CXXFLAGS="-w" cmake .. -DEVMONE_TESTING=ON && make -j4

# v4
RUN git clone --recursive --single-branch https://github.com/ethereum/evmone -b evm384-v4 evmone-evm384-v4
RUN cd evm384-v4 && mkdir build && \
  cd build && CXXFLAGS="-w" cmake .. -DEVMONE_TESTING=ON && make -j4

# v5 - v3 with curve parameters hardcoded
RUN git clone --recursive --single-branch https://github.com/ethereum/evmone -b evm384-v5 evmone-evm384-v5
RUN cd evm384-v5 && mkdir build && \
  cd build && CXXFLAGS="-w" cmake .. -DEVMONE_TESTING=ON && make -j4

WORKDIR /
CMD /bin/bash
