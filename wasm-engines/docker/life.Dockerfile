FROM ewasm/bench-build-base:1.0

LABEL maintainer="Ewasm Team"
LABEL repo="https://github.com/ewasm/benchmarking"
LABEL version="1.0"
LABEL description="Ewasm benchmarking (life)"

# install life
RUN git clone --single-branch --branch bench-times https://github.com/ewasm-benchmarking/life && \
    cd life && go mod vendor && go build
