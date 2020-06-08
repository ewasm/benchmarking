FROM ubuntu:19.10

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


RUN apt-get install -y libllvm10 llvm-10 llvm-10-dev llvm-10-doc llvm-10-examples llvm-10-runtime
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



# wabt branch for websnark-bn128 slowhost slowmont (no superops)
RUN git clone --recursive --single-branch --branch scout-bignum-hostfuncs-bn128-websnark-slowhost-slowmont https://github.com/ewasm-benchmarking/wabt.git wabt-bn128-websnark-slowmont-slowhost
RUN cd wabt-bn128-websnark-slowmont-slowhost && make clang-release
# could also use `make gcc-release`, but gcc is slower than clang

# wabt branch for websnark-bn128 slowhost slowmont superops
RUN git clone --recursive --single-branch --branch scout-bignum-hostfuncs-bn128-websnark-slowhost-slowmont-superops https://github.com/ewasm-benchmarking/wabt.git wabt-bn128-websnark-slowmont-slowhost-superops
RUN cd wabt-bn128-websnark-slowmont-slowhost-superops && make clang-release

# wabt branch for websnark-bn128 fasthost slowmont superops
RUN git clone --recursive --single-branch --branch scout-bignum-hostfuncs-bn128-websnark-fasthost-slowmont-superops https://github.com/ewasm-benchmarking/wabt.git wabt-bn128-websnark-slowmont-fasthost-superops
RUN cd wabt-bn128-websnark-slowmont-fasthost-superops && make clang-release

# wabt branch for websnark-bn128 fasthost fastmont superops
RUN git clone --recursive --single-branch --branch scout-bignum-hostfuncs-bn128-websnark-fasthost-fastmont-superops https://github.com/ewasm-benchmarking/wabt.git wabt-bn128-websnark-fastmont-fasthost-superops
RUN cd wabt-bn128-websnark-fastmont-fasthost-superops && make clang-release

# wabt branch for websnark-bn128 fasthost fastmont (no superops)
RUN git clone --recursive --single-branch --branch scout-bignum-hostfuncs-bn128-websnark-fasthost-fastmont https://github.com/ewasm-benchmarking/wabt.git wabt-bn128-websnark-fastmont-fasthost
RUN cd wabt-bn128-websnark-fastmont-fasthost && make clang-release



# the branch scout-bignums-daiquiri-withdraw is the same as scout-bignum-hostfuncs, but with a hardcoded prestate returned by eth2_loadPrestateRoot().
# the ecpairing-zkrollup-bn128 scout benchmark doesn't load the prestate, so this branch is compatible with that and with the daiquiri-withdraw benchmark
RUN git clone --recursive --single-branch --branch scout-bignums-daiquiri-withdraw https://github.com/ewasm-benchmarking/wabt.git wabt-bn128
RUN cd wabt-bn128 && make clang-release



# install wabt with bignum host fuctions for secp256k1 (no superops)
RUN git clone --recursive --single-branch --branch scout-bignum-hostfuncs-secp256k1 https://github.com/ewasm-benchmarking/wabt.git wabt-secp
RUN cd wabt-secp && make clang-release



# install wabt branch with host functions for biturbo/turbo-token-realistic (this branch has superops, but is a bit messy)
RUN git clone --recursive --single-branch --branch scout-for-biturbo-token https://github.com/ewasm-benchmarking/wabt.git wabt-biturbo
RUN cd wabt-biturbo && make clang-release

# turbo-token wabt branch without superops
RUN git clone --recursive --single-branch --branch scout-biturbo-no-superops https://github.com/ewasm-benchmarking/wabt.git wabt-biturbo-no-superops
RUN cd wabt-biturbo-no-superops && make clang-release



# wabt branch for rollup.rs bignums slowmont slowhost
RUN git clone --recursive --single-branch --branch scout-bignum-hostfuncs-bn128-rolluprs-slowmont-slowhost https://github.com/ewasm-benchmarking/wabt.git wabt-bn128-rolluprs-slowmont-slowhost
RUN cd wabt-bn128-rolluprs-slowmont-slowhost && make clang-release

# wabt branch for rollup.rs bignums slowmont slowhost superops
RUN git clone --recursive --single-branch --branch scout-bignum-hostfuncs-bn128-rolluprs-slowmont-slowhost-superops https://github.com/ewasm-benchmarking/wabt.git wabt-bn128-rolluprs-slowmont-slowhost-superops
RUN cd wabt-bn128-rolluprs-slowmont-slowhost-superops && make clang-release


# wabt branch for rollup.rs with bignums slowmont fasthost superops
# not much diff on rollup.rs, but show anyway
RUN git clone --recursive --single-branch --branch scout-bignum-hostfuncs-bn128-rolluprs-slowmont-fasthost-superops https://github.com/ewasm-benchmarking/wabt.git wabt-bn128-rolluprs-slowmont-fasthost-superops
RUN cd wabt-bn128-rolluprs-slowmont-fasthost-superops && make clang-release

# wabt branch for rollup.rs with bignum fastmont fasthost superops
# not much diff on rollup.rs, but show anyway
RUN git clone --recursive --single-branch --branch scout-bignum-hostfuncs-bn128-rolluprs-fastmont-fasthost-superops https://github.com/ewasm-benchmarking/wabt.git wabt-bn128-rolluprs-fastmont-fasthost-superops
RUN cd wabt-bn128-rolluprs-fastmont-fasthost-superops && make clang-release

# only missing rollup.rs fastmont slowhost superops

# wabt branch for rollup.rs bignums slowmont fasthost (no superops)
# not much diff on rollup.rs, ignore
#RUN git clone --recursive --single-branch --branch scout-bignum-hostfuncs-bn128-rolluprs-fastmont-fasthost https://github.com/ewasm/wabt.git wabt-bn128-rolluprs-fastmont-fasthost
#RUN cd wabt-bn128-rolluprs-fastmont-fasthost && make clang-release

# wabt branch for rollup.rs bignums fastmont fasthost (no superops)
# not much diff on rollup.rs, ignore
#RUN git clone --recursive --single-branch --branch scout-bignum-hostfuncs-bn128-rolluprs-fastmont-fasthost https://github.com/ewasm/wabt.git wabt-bn128-rolluprs-fastmont-fasthost
#RUN cd wabt-bn128-rolluprs-fastmont-fasthost && make clang-release

# wabt branch for rollup.rs bignum fastmont slowhost (no superops)
# not much diff on rollup.rs, ignore
#RUN git clone --recursive --single-branch --branch scout-bignum-hostfuncs-bn128-rolluprs-fastmont-slowhost https://github.com/ewasm/wabt.git wabt-bn128-rolluprs-fastmont-slowhost
#RUN cd wabt-bn128-rolluprs-fastmont-slowhost && make clang-release


# wabt branch for wasmsnark bls12
RUN git clone --recursive --single-branch --branch bls12-bignums-fastmont-superops https://github.com/ewasm/wabt.git wabt-bls12-fastmont-fasthost-superops
RUN cd wabt-bls12-fastmont-fasthost-superops && make clang-release

# for the "host func variations" (i.e. using host funcs for [f1m_mul], [f1m_mul, f1m_add], [f1m_mul, f1m_add, f1m_sub], ...)
# we need to use the no-superops wabt branch because there's a bug in superops triggered by the wasm code in one of {int_mul, int_sub, int_add, int_div} (I can't remember which)
RUN git clone --recursive --single-branch --branch bls12-bignums-fasthost-fastmont-no-superops https://github.com/ewasm/wabt.git wabt-bls12-bignums-fasthost-fastmont-no-superops
RUN cd wabt-bls12-bignums-fasthost-fastmont-no-superops && make clang-release


# Note: these scout.cpp branches are disabled because the wabt version scout.cpp is based on is slower than the wabt version used in the `github.com/ewasm/wabt` branches
# We don't know why scout.cpp is slower than `github.com/ewasm/wabt`, in theory it should be the same speed.
# scout.cpp is based on a later version of wabt (wabt-2020), `github.com/ewasm/wabt` is an older version (wabt-2018).
# There might be a performance regression in later versions of wabt.

# install scout.cpp branch with bignum host functions for bn128
#RUN git clone --recursive --single-branch --branch bignum-host-funcs https://github.com/ewasm-benchmarking/scout_wabt.cpp.git scoutcpp-bn128
# commit 7afd65dda637436151d69fb47d22034c2ecfea45 (fix interleaved)
#RUN cd scoutcpp-bn128 && mkdir build && cd build && cmake -DBUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release .. && make

# install scout.cpp branch with bignum host functions for secp256k1
#RUN git clone --recursive --single-branch --branch bignum-hostfuncs-secp256k1 https://github.com/ewasm-benchmarking/scout_wabt.cpp.git scoutcpp-secp
#RUN cd scoutcpp-secp && mkdir build && cd build && cmake -DBUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release .. && make

# install scout.cpp branch for rollup.rs
#RUN git clone --recursive --single-branch --branch bignum-hostfuncs-bn128-rolluprs https://github.com/ewasm-benchmarking/scout_wabt.cpp.git scoutcpp-bn128-rolluprs
#RUN cd scoutcpp-bn128-rolluprs && mkdir build && cd build && cmake -DBUILD_TESTS=OFF -DCMAKE_BUILD_TYPE=Release .. && make


WORKDIR /scoutyamls

# clone scout.ts branch with secp-sig-verify
RUN git clone https://github.com/ewasm-benchmarking/scout.ts.git --single-branch --branch secp-sig-verify scout.ts-secp
RUN cd scout.ts-secp && npm install && npm run build

# clone scout.ts branch with bn128-pairing
RUN git clone https://github.com/ewasm-benchmarking/scout.ts.git --single-branch --branch bn128-pairing scout.ts-bn128
RUN cd scout.ts-bn128 && npm install && npm run build

# clone daiquri branch
RUN git clone https://github.com/ewasm-benchmarking/daiquiri.git --single-branch --branch scout-benchreport-withdraw daiquiri
RUN cd daiquiri && npm install && npm run build

# clone biturbo branch
RUN git clone https://github.com/ewasm-benchmarking/biturbo.git --single-branch --branch scout-benchreport biturbo
RUN cd biturbo && npm install && npm run build
RUN cd biturbo && npm run token:relayer:realistic && npm run token:build

# TODO: for the bls12 branch (and probably the other scout.ts branches), doing `npm run build` in the scout.ts dir
# will build the scout.ts runner. In `scout.ts/assembly/bls12-pairing`, `npm run build` will build the wasm file.
# Building the wasm file is currently fragile, and won't work if the right `asc` version isn't installed.
# Need to investigate what the right `asc` version is, or fix so it builds on later asc versions.
# For now, the wasm builds are pushed to the repo. The `npm run build` below only builds the scout.ts runner.

# clone scout.ts branch with bls12
RUN git clone https://github.com/ewasm/scout.ts.git --single-branch --branch bls12-bench-report scout.ts-bls12
RUN cd scout.ts-bls12 && npm install && npm run build


# clone c_ewasm_contracts (commit 29356a22ea38cf2f1bbab05a4b8974822834f4e7)
RUN git clone https://github.com/ewasm-benchmarking/C_ewasm_contracts.git --single-branch --branch master C_ewasm_contracts
# remove some tests we don't want
RUN cd C_ewasm_contracts/tests && rm ecrecover.yaml ecrecover_trezor.yaml ed25519verify.yaml helloworld.yaml


# install rust
RUN curl https://sh.rustup.rs -sSf | \
    sh -s -- --default-toolchain stable -y && . $HOME/.cargo/env
ENV PATH=/root/.cargo/bin:$PATH

RUN rustup default 1.36.0

# rust wasm32 target for compiling wasm
RUN rustup target add wasm32-unknown-unknown


# clone rollup.rs native
RUN git clone https://github.com/ewasm-benchmarking/rollup.rs --single-branch --branch benchreport-rust-native rollup-rs-native
RUN cd rollup-rs-native && cargo build --release

# clone rollup.rs scout no bignums
RUN git clone https://github.com/ewasm-benchmarking/rollup.rs --single-branch --branch benchreport-scout-no-bignums rollup-rs-no-bignums
RUN cd rollup-rs-no-bignums && cargo build --lib --release
RUN cd /scoutyamls/scout.ts-bn128 && mkdir -p target/wasm32-unknown-unknown/release
RUN cd /scoutyamls/scout.ts-bn128 && cp /scoutyamls/rollup-rs-no-bignums/target/wasm32-unknown-unknown/release/rollup_rs_wasm.wasm ./target/wasm32-unknown-unknown/release/rollup_rs_wasm.wasm
RUN cp /scoutyamls/rollup-rs-no-bignums/rolluprs.yaml /scoutyamls/scout.ts-bn128/rolluprs.yaml

# clone rollup.rs for scout with bignums
RUN git clone https://github.com/ewasm-benchmarking/rollup.rs --single-branch --branch benchreport-scout-bignums rollup-rs-with-bignums
RUN cd rollup-rs-with-bignums && cargo build --lib --release

RUN rustup default nightly-2020-04-23

# clone eip1962-bls12.rs native
RUN git clone --single-branch --branch dev https://github.com/jwasinger/eip1962-bls12-381-bench.git eip1962-bls12-rs-native
RUN cd eip1962-bls12-rs-native && git submodule update --init
RUN cd eip1962-bls12-rs-native && cargo build --release


# install fizzy
WORKDIR /engines

# magic to install cmake 13.5 on ubuntu 19.10
RUN wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | gpg --dearmor - | sudo tee /etc/apt/trusted.gpg.d/kitware.gpg >/dev/null && \
  wget http://archive.ubuntu.com/ubuntu/pool/main/o/openssl1.0/libssl1.0.0_1.0.2n-1ubuntu5.3_amd64.deb && \
  dpkg -i libssl1.0.0_1.0.2n-1ubuntu5.3_amd64.deb && \
  apt-add-repository 'deb https://apt.kitware.com/ubuntu/ xenial main' && \
  apt-get update && \
  apt-get install -y cmake-data=3.15.5-0kitware1 && \
  apt-get install -y cmake=3.15.5-0kitware1


# fizzy for bls12 using host funcs
RUN git clone --single-branch --branch ewasm-bench-bls12 https://github.com/wasmx/fizzy.git fizzy-bls12-hostfuncs && \
  cd fizzy-bls12-hostfuncs && \
  mkdir build && cd build && \
  cmake -DFIZZY_TESTING=ON .. && \
  cmake --build .

RUN cd fizzy-bls12-hostfuncs/build/bin && mkdir bls12-synth-loop && \
  echo -e "synth\nmain\n:\n\n\n\n" > bls12-synth-loop/main_with_websnark_bignum_hostfuncs.inputs && \
  mkdir bls12-pairing && mkdir bls12-pairing-nohostfuncs && \
  echo -e "synth\nmain\n:\n\n\n\n" > bls12-pairing/main_with_websnark_bignum_hostfuncs.inputs && \
  echo -e "synth\nmain\n:\n\n\n\n" > bls12-pairing-nohostfuncs/main_with_websnark.inputs


# get non-scout/standalone builds of wasmsnark
WORKDIR /scoutyamls

RUN git clone https://github.com/ewasm/scout.ts.git --single-branch --branch f6m_mul_loop-standalone scout.ts-bls12-standalone-synth-loop
RUN git clone https://github.com/ewasm/scout.ts.git --single-branch --branch bls12-bench-standalone scout.ts-bls12-standalone-pairing


# copy wasm files to fizzy dir
RUN cp /scoutyamls/scout.ts-bls12-standalone-synth-loop/assembly/bls12-pairing/out/main_with_websnark_bignum_hostfuncs.wasm /engines/fizzy-bls12-hostfuncs/build/bin/bls12-synth-loop && \
  cp /scoutyamls/scout.ts-bls12-standalone-pairing/assembly/bls12-pairing/out/main_with_websnark_bignum_hostfuncs.wasm /engines/fizzy-bls12-hostfuncs/build/bin/bls12-pairing && \
  cp /scoutyamls/scout.ts-bls12-standalone-pairing/assembly/bls12-pairing/out/main_with_websnark.wasm /engines/fizzy-bls12-hostfuncs/build/bin/bls12-pairing-nohostfuncs

# copy the python script to run the benchmarks
RUN mkdir /benchscript
COPY nanodurationpy.py /benchscript
COPY scout_bignum_bench.py /benchscript

# benchmark_results_data should be a mounted volume
RUN mkdir -p /benchmark_results_data

WORKDIR /benchscript

CMD /bin/bash
