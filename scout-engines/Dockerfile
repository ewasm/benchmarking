FROM ubuntu:19.04

# System deps
RUN apt-get clean
RUN apt-get update
RUN apt-get install -y software-properties-common git sudo build-essential wget curl nano \
    autoconf automake libtool make ninja-build unzip zlib1g-dev texinfo libssl-dev

RUN sudo apt-get clean autoclean
RUN sudo apt-get autoremove -y


RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add - && \
    apt-add-repository "deb http://apt.llvm.org/disco/ llvm-toolchain-disco-10 main" && \
    apt-get update


RUN apt-get install -y libllvm-10-ocaml-dev libllvm10 llvm-10 llvm-10-dev llvm-10-doc llvm-10-examples llvm-10-runtime
RUN apt-get install -y clang-10 clang-tools-10 clang-10-doc libclang-common-10-dev libclang-10-dev libclang1-10 clang-format-10
RUN apt-get install -y lldb-10 lld-10 libc++-10-dev libc++abi-10-dev


# comment out all this to use gcc instead of clang
RUN update-alternatives --install /usr/bin/c++ c++ /usr/bin/clang++-10 60
RUN update-alternatives --install /usr/bin/clang++ clang++ /usr/bin/clang++-10 60
RUN update-alternatives --install /usr/bin/clang clang /usr/bin/clang-10 60
RUN update-alternatives --install /usr/bin/llvm-ar llvm-ar /usr/bin/llvm-ar-10 60
RUN update-alternatives --install /usr/bin/llvm-nm llvm-nm /usr/bin/llvm-nm-10 60
RUN update-alternatives --install /usr/bin/llvm-ranlib llvm-ranlib /usr/bin/llvm-ranlib-10 60
RUN update-alternatives --install /usr/bin/ld ld.lld-10 /usr/bin/ld.lld-10 60


RUN apt-get install -y cmake

RUN apt-get install -y python # python2.7 needed to build wabt

RUN apt-get install -y python3 python3-distutils
RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py

## pandas needed for nanodurationpy (for the benchmarking script)
RUN pip3 install pandas


WORKDIR /engines

# install node 12
RUN curl -sL https://deb.nodesource.com/setup_12.x | bash
RUN apt-get install -y nodejs


# install google benchmark lib, needed for wabt-secp
RUN git clone https://github.com/google/benchmark.git google-benchmark
# commit 8e0b1913d4ea803dfeb2e55567208fcab6b1b6c7
RUN git clone https://github.com/google/googletest.git google-benchmark/googletest
RUN cd google-benchmark && mkdir build
#RUN cd google-benchmark/build && cmake -DCMAKE_BUILD_TYPE=Release -DBENCHMARK_ENABLE_LTO=true ../
# we need BENCHMARK_USE_LIBCXX=true because we're going to use clang to compile wabt
RUN cd google-benchmark/build && cmake -DCMAKE_BUILD_TYPE=Release -DBENCHMARK_USE_LIBCXX=true ../
RUN cd google-benchmark/build && make -j8
RUN cd google-benchmark/build && make install



# install wabt with bignum host fuctions for bn128
#RUN git clone --recursive --single-branch --branch scout-bignum-hostfuncs https://github.com/ewasm/wabt.git wabt-bn128
# the branch scout-bignums-daiquiri-withdraw is the same as scout-bignum-hostfuncs, but with a hardcoded prestate returned by eth2_loadPrestateRoot().
# the ecpairing-zkrollup-bn128 scout benchmark doesn't load the prestate, so this branch is compatible with that and with the daiquiri-withdraw benchmark
RUN git clone --recursive --single-branch --branch scout-bignums-daiquiri-withdraw https://github.com/ewasm/wabt.git wabt-bn128
RUN cd wabt-bn128 && make clang-release
# could also use `make gcc-release`, but gcc is slower than clang

# install wabt with bignum host fuctions for secp256k1
RUN git clone --recursive --single-branch --branch scout-bignum-hostfuncs-secp256k1 https://github.com/ewasm/wabt.git wabt-secp
RUN cd wabt-secp && make clang-release

## TODO: clean up this wabt branch. install two versions: with-superops and no-superops
# install wabt branch with host functions for biturbo/turbo-token-realistic
RUN git clone --recursive --single-branch --branch scout-for-biturbo-token https://github.com/ewasm/wabt.git wabt-biturbo
RUN cd wabt-biturbo && make clang-release


# install scout.cpp branch with bignum host functions for bn128
RUN git clone --recursive --single-branch --branch bignum-host-funcs https://github.com/cdetrio/scout.cpp.git scoutcpp-bn128
# commit 7afd65dda637436151d69fb47d22034c2ecfea45 (fix interleaved)
RUN cd scoutcpp-bn128 && mkdir build && cd build && cmake -DBUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release .. && make

# install scout.cpp branch with bignum host functions for secp256k1
RUN git clone --recursive --single-branch --branch bignum-hostfuncs-secp256k1 https://github.com/cdetrio/scout.cpp.git scoutcpp-secp
RUN cd scoutcpp-secp && mkdir build && cd build && cmake -DBUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release .. && make




WORKDIR /scoutyamls

# clone scout.ts branch with secp-sig-verify
RUN git clone https://github.com/ewasm/scout.ts.git --single-branch --branch secp-sig-verify scout.ts-secp
RUN cd scout.ts-secp && npm install && npm run build

# clone scout.ts branch with bn128-pairing
RUN git clone https://github.com/ewasm/scout.ts.git --single-branch --branch bn128-pairing scout.ts-bn128
RUN cd scout.ts-bn128 && npm install && npm run build

# clone daiquri branch
RUN git clone https://github.com/cdetrio/daiquiri.git --single-branch --branch scout-benchreport-withdraw daiquiri
RUN cd daiquiri && npm install && npm run build

# clone biturbo branch
RUN git clone https://github.com/ewasm/biturbo.git --single-branch --branch scout-benchreport biturbo
RUN cd biturbo && npm install && npm run build
RUN cd biturbo && npm run token:relayer:realistic && npm run token:build



# copy the python script to run the benchmarks
RUN mkdir /benchscript
COPY nanodurationpy.py /benchscript
COPY scout_bignum_bench.py /benchscript

# benchmark_results_data should be a mounted volume
RUN mkdir -p /benchmark_results_data

WORKDIR /benchscript

CMD /bin/bash
