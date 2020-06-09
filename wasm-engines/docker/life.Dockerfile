FROM ewasm/bench-build-base:1.0

# install life
RUN git clone --single-branch --branch bench-times https://github.com/ewasm-benchmarking/life && \
    cd life && go mod vendor && go build
