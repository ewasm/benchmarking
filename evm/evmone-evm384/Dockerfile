FROM ewasm/bench-build-base:1

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1"
LABEL description="Ewasm benchmarking (evmone-evm384)"

RUN pip3 install durationpy pandas

# install evmone (need CXXFLAGS=-w or the build fails)
WORKDIR /root
RUN git clone --recursive --single-branch --branch v0.5.0-evm384-v1 https://github.com/ethereum/evmone.git evmone-evm384-v1
RUN cd evmone-evm384-v1 && mkdir build && \
  cd build && CXXFLAGS="-w" cmake .. -DEVMONE_TESTING=ON && make -j4

RUN git clone --recursive --single-branch --branch v0.5.0-evm384-v2 https://github.com/ethereum/evmone.git evmone-evm384-v2
RUN cd evmone-evm384-v2 && mkdir build && \
  cd build && CXXFLAGS="-w" cmake .. -DEVMONE_TESTING=ON && make -j4

# evmone branch with mem check disabled
RUN git clone --recursive --single-branch https://github.com/ethereum/evmone -b v0.5.0-evm384-v2-unsafe evmone-evm384-v2-unsafe
RUN cd evmone-evm384-v2-unsafe && mkdir build && \
  cd build && CXXFLAGS="-w" cmake .. -DEVMONE_TESTING=ON && make -j4

# evmone branch with curve params hard coded
RUN git clone --recursive --single-branch https://github.com/jwasinger/evmone -b v2-no-curve-params evmone-evm384-v2-no-curve-params
RUN cd evmone-evm384-v2-no-curve-params && mkdir build && \
  cd build && CXXFLAGS="-w" cmake .. -DEVMONE_TESTING=ON && make -j4

# fetch evm384 f6m_mul synthetic loop repo
RUN git clone --single-branch --branch v0.0.1 https://github.com/ewasm/evm384_f6m_mul.git

# branch that pre-allocates a page of memory to remain safe (because mem check is disabled)
RUN git clone --single-branch --branch mem-check-disable https://github.com/ewasm/evm384_f6m_mul.git mem-check-disable-evm384_f6m_mul

# evm384 branch with curve params hardcoded
RUN git clone --single-branch --branch v2-no-curve-parameters https://github.com/ewasm/evm384_f6m_mul v2-no-curve-params-evm384_f6m_mul

WORKDIR /
CMD /bin/bash
