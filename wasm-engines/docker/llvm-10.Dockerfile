FROM ewasm/bench-build-base:1.0

RUN echo "deb http://apt.llvm.org/focal/ llvm-toolchain-focal-10 main\
    deb-src http://apt.llvm.org/focal/ llvm-toolchain-focal-10 main" >> /etc/apt/sources.list && \
    wget -O - https://apt.llvm.org/llvm-snapshot.gpg.key|sudo apt-key add - && apt update -y && apt install -y clang-10 lldb-10 lld-10 && \
    ln -s /usr/bin/clang++-10  /usr/bin/clang++ && \
    ln -s /usr/bin/clang-10  /usr/bin/clang

ENV CC=clang
ENV CXX=clang++
