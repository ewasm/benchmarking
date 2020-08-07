FROM ewasm/life:1 AS life
FROM ewasm/wabt:1 AS wabt
FROM ewasm/wasm3:1 AS wasm3
FROM ewasm/ssvm:1 AS ssvm
FROM ewasm/wasmtime:1 AS wasmtime
FROM ewasm/wamr:1 AS wamr
FROM ewasm/wagon:1 AS wagon
FROM ewasm/wavm:1 AS wavm
FROM ewasm/fizzy:1 AS fizzy
FROM ewasm/asmble:1 AS asmble
FROM ewasm/wasmi:1 AS wasmi
FROM ewasm/vanilla-wabt:1 AS vanilla-wabt

FROM ewasm/llvm-10:1

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1"
LABEL description="Benchmarking environment for Ewasm benchmarking"

# install dependencies for standalone wasm prep
RUN pip3 install jinja2 pandas click durationpy

# install JRE for asmble
RUN apt update -y && apt install -y openjdk-8-jre
ENV JAVA_VER 8
ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64

RUN mkdir /engines

# install node for v8 benchmarks
RUN curl -fsSLO --compressed https://nodejs.org/download/release/v12.18.2/node-v12.18.2-linux-x64.tar.gz && \
  tar -xvf node-v12.18.2-linux-x64.tar.gz -C /usr/local/ --strip-components=1 --no-same-owner
RUN mkdir /engines/node && ln -s /usr/local/bin/node /engines/node/node

# wasm engine binaries
COPY --from=wabt /wabt/build/wasm-interp /engines/wabt/wasm-interp
COPY --from=vanilla-wabt /vanilla-wabt/build/wasm-interp /engines/vanilla-wabt/wasm-interp
COPY --from=fizzy /fizzy/build/bin/fizzy-bench /engines/fizzy/fizzy-bench
COPY --from=wasmi /wasmi/target/release/invoke /engines/wasmi/invoke
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

RUN mkdir /benchmark_results_data

# copy benchmarking scripts
RUN mkdir /benchrunner

# copy scripts to generate standalone wasm modules
RUN mkdir /benchprep

WORKDIR /benchprep

CMD /bin/bash
