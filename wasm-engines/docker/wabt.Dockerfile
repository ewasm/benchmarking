FROM ewasm/llvm-10:1.0

RUN git clone --recursive --single-branch --branch bench-times https://github.com/ewasm-benchmarking/wabt.git && \
    mkdir wabt/build && cd wabt/build && cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTS=OFF .. && make
