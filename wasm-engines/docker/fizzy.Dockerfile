FROM ewasm/llvm-10:1.0

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1.0"
LABEL description="Ewasm benchmarking (fizzy)"

# install fizzy
RUN git clone https://github.com/wasmx/fizzy.git --single-branch --branch v0.1.0 && \
    cd fizzy && mkdir build && cd build && cmake -DNATIVE=ON -DFIZZY_TESTING=ON .. && cmake --build .
