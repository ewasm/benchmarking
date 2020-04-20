FROM ubuntu:19.04

# System deps
RUN apt-get clean
RUN apt-get update
RUN apt-get install -y software-properties-common git sudo build-essential wget curl nano \
    autoconf automake libtool llvm-6.0 make ninja-build unzip zlib1g-dev texinfo libssl-dev

# Install CMake
RUN wget https://github.com/Kitware/CMake/releases/download/v3.16.4/cmake-3.16.4.tar.gz
RUN tar -xzvf cmake-3.16.4.tar.gz
RUN cd cmake-3.16.4 && ./bootstrap && make && make install

# install python 2.7
RUN apt-get install -y python2.7

# install python 3.7
RUN apt-get install -y python3.7
RUN apt-get install -y python3-distutils
RUN wget https://bootstrap.pypa.io/get-pip.py && python3.7 get-pip.py

# Install Go 1.11 (update 2019-03-16: now installs go 1.12)
RUN add-apt-repository ppa:longsleep/golang-backports && apt-get update && apt-get install -y golang-go

# enable go modules: https://github.com/golang/go/wiki/Modules
RUN export GO111MODULE=on

RUN sudo apt-get clean autoclean
RUN sudo apt-get autoremove -y

# Install Clang 8 (needed for life -polymerase)
RUN apt install -y clang-8 lldb-8 lld-8

RUN ln -s /usr/bin/clang-8 /usr/bin/clang && \
    ln -s /usr/bin/clang++-8 /usr/bin/clang++

WORKDIR /engines

# install life
RUN git clone --single-branch --branch bench-times https://github.com/cdetrio/life
RUN cd life && go mod vendor
RUN cd life && go build


# install wagon
RUN git clone --single-branch --branch bench-times https://github.com/cdetrio/wagon
RUN cd wagon/cmd/wasm-run && go build

# install rust
RUN curl https://sh.rustup.rs -sSf | \
    sh -s -- --default-toolchain stable -y && . $HOME/.cargo/env
ENV PATH=/root/.cargo/bin:$PATH

RUN rustup default 1.31.0

# install wasmi
RUN git clone --single-branch --branch bench-time https://github.com/cdetrio/wasmi.git --recursive
RUN cd wasmi && cargo test --release

# Use old gcc/g++ for wavm (needed by wavm)
RUN apt install -y gcc-7
RUN apt install -y g++-7
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-7 10
RUN update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-7 10

# install wavm
RUN git clone --single-branch --branch bench-compile-time https://github.com/cdetrio/WAVM
RUN mkdir wavm-build
RUN cd wavm-build && cmake -G Ninja ../WAVM -DCMAKE_BUILD_TYPE=RelWithDebInfo
RUN cd wavm-build && ninja


# install binaryen
#RUN git clone https://github.com/WebAssembly/binaryen.git
#RUN cd binaryen && cmake . && make


## wasmer superseded by wasmtime
# install wasmer
# download wasmer binary
#RUN curl https://get.wasmer.io -sSfL | sh
#RUN /bin/bash -c "source /root/.wasmer/wasmer.sh"
# build wasmer from source
# wasmer release 0.1.4 has segmentation violation with rustc 1.32.0. use 1.31.1
#RUN rustup default 1.31.1
#  0.1.4 release from December 2018 is faster than latest wasmer master (2019-2-16) 
#RUN git clone --single-branch --branch bench-release https://github.com/cdetrio/wasmer.git
#RUN cd wasmer && cargo build --release
# bug where running wasmer v0.1.4 with python `Popen(stderr=subprocess.STDOUT)`
# causes an error: `Runtime error: trap at 0x0 - illegal instruction`.
# the fix is to run Popen without the stderr flag.
#RUN rustup default nightly-2019-01-15
#RUN git clone --single-branch --branch bench-compile-time https://github.com/cdetrio/wasmer.git wasmer-master
#RUN cd wasmer-master && cargo build --release


# install wasmtime
RUN rustup default nightly-2019-01-15
RUN git clone --single-branch --branch bench-times https://github.com/cdetrio/wasmtime.git
RUN cd wasmtime && cargo build --release


# install wabt
RUN git clone --recursive --single-branch --branch bench-times https://github.com/cdetrio/wabt.git
RUN mkdir wabt/build && cd wabt/build && cmake -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTS=OFF .. && make


# install python modules needed for benchmarking script
RUN pip3 install click durationpy


# install nodejs
#RUN mkdir node
RUN mkdir -p node
RUN cd node && curl -fsSLO --compressed https://nodejs.org/dist/v11.10.0/node-v11.10.0-linux-x64.tar.gz
RUN cd node && tar -xvf node-v11.10.0-linux-x64.tar.gz -C /usr/local/ --strip-components=1 --no-same-owner
RUN cd node && ln -s /usr/local/bin/node ./node
COPY node-timer.js ./node/node-timer.js

# curl -fsSLO --compressed https://nodejs.org/download/nightly/v12.0.0-nightly20190325cdb87d9548/node-v12.0.0-nightly20190325cdb87d9548-linux-x64.tar.gz


# install java
# ENV JAVA_VER 8
# ENV JAVA_HOME /usr/lib/jvm/java-8-oracle

# RUN \
#  echo oracle-java8-installer shared/accepted-oracle-license-v1-1 select true | debconf-set-selections && \
#  add-apt-repository -y ppa:webupd8team/java && \
#  apt-get update && \
#  apt-get install -y oracle-java8-installer && \
#  rm -rf /var/lib/apt/lists/* && \
#  rm -rf /var/cache/oracle-jdk8-installer

# ENV JAVA_HOME /usr/lib/jvm/java-8-oracle


#RUN echo 'deb http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main' >> /etc/apt/sources.list && \
#    echo 'deb-src http://ppa.launchpad.net/webupd8team/java/ubuntu trusty main' >> /etc/apt/sources.list 

#RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys C2518248EEA14886
#RUN apt-get update
#RUN echo oracle-java${JAVA_VER}-installer shared/accepted-oracle-license-v1-1 select true | sudo /usr/bin/debconf-set-selections 

#RUN apt-get install -y --force-yes --no-install-recommends oracle-java${JAVA_VER}-installer oracle-java${JAVA_VER}-set-default 
#RUN apt-get clean 
#RUN rm -rf /var/cache/oracle-jdk${JAVA_VER}-installer

# install asmble
#RUN wget https://github.com/cdetrio/asmble/releases/download/0.4.2-fl-bench-times/asmble-0.4.2-fl-bench-times.tar
#RUN tar -xvf asmble-0.4.2-fl-bench-times.tar

# install wag
#RUN apt-get install -y libcapstone-dev
#RUN git clone --single-branch --branch runtime-design https://github.com/gballet/wag.git
#RUN cd wag && go build ./cmd/ethereum/...

# install wamr (interpreter, aot, jit)
RUN git clone https://github.com/hugo-dc/wasm-micro-runtime.git --single-branch --branch benchmark
RUN cd wasm-micro-runtime && git pull origin benchmark
## Build LLVM
RUN cd wasm-micro-runtime/product-mini/platforms/linux && ./build_llvm.sh 
## Build JIT
RUN cd wasm-micro-runtime/product-mini/platforms/linux && ./build_jit.sh 
## Build Interpreter
RUN cd wasm-micro-runtime/product-mini/platforms/linux && mkdir build_interp && cd build_interp && cmake -DWAMR_BUILD_INTERP=1 .. -DCMAKE_BUILD_TYPE=Release .. && make
## Build Compiler
RUN cd wasm-micro-runtime/wamr-compiler && mkdir build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make

# install wasm3
RUN git clone https://github.com/hugo-dc/wasm3.git --single-branch --branch benchmark
RUN cd wasm3 && mkdir build && cd build && cmake -DCMAKE_BUILD_TYPE=Release .. && make

# Update gcc/g++
RUN update-alternatives --remove-all gcc
RUN update-alternatives --remove-all g++
RUN apt install -y gcc-9
RUN apt install -y g++-9

RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-9 1
RUN update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-9 1

# install fizzy
RUN git clone https://github.com/wasmx/fizzy.git --single-branch --branch master
RUN cd fizzy && mkdir build && cd build && cmake -DFIZZY_TESTING=ON .. && cmake --build .


## install dependencies for standalone wasm prep
RUN pip3 install jinja2 pandas

# rust wasm32 target for compiling wasm
RUN rustup target add wasm32-unknown-unknown

# copy benchmarking scripts
RUN mkdir /benchrunner
COPY main.py /benchrunner
COPY wamr_aot.sh /engines/wasm-micro-runtime/
COPY fizzy.sh /engines/fizzy/

# copy scripts to generate standalone wasm modules
RUN mkdir /benchprep

RUN mkdir -p /benchmark_results_data

WORKDIR /benchprep

CMD /bin/bash

