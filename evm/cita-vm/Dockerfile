FROM ewasm/bench-build-base:1

RUN pip3 install durationpy jinja2 pandas

# install cita-vm
RUN git clone --single-branch --branch v0.1.3-benchmarking https://github.com/ewasm-benchmarking/cita-vm
RUN cd cita-vm/evmbin && cargo build --release
