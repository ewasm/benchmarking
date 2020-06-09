FROM ewasm/llvm-10:1.0

# install fizzy
RUN git clone https://github.com/wasmx/fizzy.git --single-branch --branch v0.1.0 && \
    cd fizzy && mkdir build && cd build && cmake -DNATIVE=ON -DFIZZY_TESTING=ON .. && cmake --build .
