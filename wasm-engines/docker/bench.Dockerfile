FROM ewasm/life:1.0 as life
FROM ewasm/wabt:1.0 as wabt
FROM ewasm/wasm3:1.0 as wasm3
FROM ewasm/ssvm:1.0 as ssvm
FROM ewasm/wasmtime:1.0 as wasmtime
FROM ewasm/wamr:1.0 as wamr
FROM ewasm/wagon:1.0 as wagon
FROM ewasm/wavm:1.0 as wavm
FROM ewasm/fizzy:1.0 as fizzy
FROM ewasm/asmble:1.0 as asmble
FROM ewasm/wasmi:1.0 as wasmi

FROM ewasm/bench-build-base:1.0

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1.0"
LABEL description="Benchmarking environment for Ewasm benchmarking"

## install dependencies for standalone wasm prep
RUN pip3 install jinja2 pandas click durationpy

RUN echo "deb http://apt.llvm.org/focal/ llvm-toolchain-focal-10 main\
    deb-src http://apt.llvm.org/focal/ llvm-toolchain-focal-10 main" >> /etc/apt/sources.list
RUN wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key|sudo apt-key add - && apt update -y && apt install -y clang-10 lldb-10 lld-10

RUN ln -s /usr/bin/clang++-10  /usr/bin/clang++
RUN ln -s /usr/bin/clang-10  /usr/bin/clang

ENV CC=clang
ENV CXX=clang++

ENV JAVA_VER 8
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

# rust wasm32 target for compiling wasm
RUN rustup target add wasm32-unknown-unknown

RUN mkdir -p /benchmark_results_data && mkdir /engines

# install node for v8 benchmarks
RUN curl -fsSLO --compressed https://nodejs.org/dist/v11.10.0/node-v11.10.0-linux-x64.tar.gz && \
  tar -xvf node-v11.10.0-linux-x64.tar.gz -C /usr/local/ --strip-components=1 --no-same-owner

# install JRE for asmble
RUN apt install -y openjdk-8-jre

# wasm engine binaries
COPY --from=wabt /wabt/build/wasm-interp /engines/wabt/wasm-interp
COPY --from=fizzy /fizzy/build/bin/fizzy-bench /engines/fizzy/fizzy-bench
COPY --from=wasmi /wasmi/target/release/examples/invoke /engines/wasmi/invoke

COPY --from=wavm  /wavm-build/ /engines/wavm
RUN cd /engines/wavm/Lib && find . -name "*.so" -exec cp -prv '{}' '/usr/lib' ';'

COPY --from=life  /life/life /engines/life/life
COPY --from=wasm3 /wasm3/build/wasm3 /engines/wasm3/wasm3
COPY --from=wasmtime /wasmtime/target/release/wasmtime /engines/wasmtime/wasmtime
COPY --from=ssvm /SSVM/build/tools/ssvm/ssvm /engines/ssvm/ssvm

COPY --from=wamr /wasm-micro-runtime/product-mini/platforms/linux/build_interp/iwasm /engines/wamr/iwasm
COPY --from=wamr /wasm-micro-runtime/wamr-compiler/build/wamrc /engines/wamr/wamrc
COPY --from=asmble /asmble/ /engines/asmble/
COPY --from=wagon /wagon/cmd/wasm-run/wasm-run /engines/wagon/wasm-run

# copy benchmarking scripts
RUN mkdir /benchrunner

RUN mkdir /engines/node && ln -s /usr/local/bin/node /engines/node/node 

# copy scripts to generate standalone wasm modules
RUN mkdir /benchprep

WORKDIR /benchprep

CMD /bin/bash
