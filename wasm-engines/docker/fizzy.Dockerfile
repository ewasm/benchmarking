FROM ewasm/llvm-10:1 AS build

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1"
LABEL description="Ewasm benchmarking (fizzy)"

# install fizzy
RUN git clone https://github.com/wasmx/fizzy.git --single-branch --branch v0.3.0 && \
    cd fizzy && mkdir build && cd build && cmake -DNATIVE=ON -DFIZZY_TESTING=ON .. && make -j4

FROM ewasm/bench-build-base:1
COPY --from=build /fizzy/build/bin/ /fizzy/build/bin
