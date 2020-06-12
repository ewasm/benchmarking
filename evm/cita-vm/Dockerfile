FROM ewasm/bench-build-base:1

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1"
LABEL description="Ewasm benchmarking (cita-vm)"

RUN pip3 install durationpy jinja2 pandas

# install cita-vm
RUN git clone --single-branch --branch v0.1.3-benchmarking https://github.com/ewasm-benchmarking/cita-vm
RUN cd cita-vm/evmbin && cargo build --release
