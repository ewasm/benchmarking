FROM ewasm/bench-build-base:1 AS build

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1"
LABEL description="Ewasm benchmarking (eos-vm)"

# install eos-vm
RUN git clone --single-branch --branch v10.14.6-benchmarking https://github.com/ewasm-benchmarking/eos-vm && \
    cd eos-vm/ && mkdir build && cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release -DENABLE_SOFTFLOAT=OFF -DUSE_EXISTING_BOOST=ON .. && \
    make 

FROM ewasm/bench-build-base:1
COPY --from=build /eos-vm/build/tools/bench-interp /eos-vm/build/tools/bench-interp
