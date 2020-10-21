FROM ewasm/bench-build-base:1 AS build

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1"
LABEL description="Ewasm benchmarking (wavm)"

# Use old gcc/g++ for wavm (needed by wavm)
RUN apt install -y gcc-7 g++-7 &&  \
    update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 10 && \
    update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-7 10 && \
# install wavm
    git clone --single-branch --branch bench-compile-time https://github.com/ewasm-benchmarking/WAVM && \
    mkdir wavm-build && \
    cd wavm-build && cmake -G Ninja ../WAVM -DCMAKE_BUILD_TYPE=Release -DWAVM_ENABLE_STATIC_LINKING=ON && \
    ninja

FROM ewasm/bench-build-base:1
COPY --from=build /wavm-build /wavm-build
