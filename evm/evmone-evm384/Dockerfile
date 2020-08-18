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

# fetch evm384 f6m_mul synthetic loop repo
RUN git clone --single-branch --branch f6m_mul_native https://github.com/ewasm/evm384_f6m_mul.git

RUN cd evm384_f6m_mul && \
	git submodule update --init && \
	cd src/native && \
	mkdir build && \
	cd build && \
	cmake -DCMAKE_BUILD_TYPE=RELEASE .. && \
	make -j4

WORKDIR /
CMD /bin/bash
