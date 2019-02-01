This directory contains source for wasm performance benchmarks.  These benchmarks do not conform to the EWASM EEI and are meant to be run standalone

#Build
`cargo build --target wasm32-unknown-unknown`

#Run
* [Life](https://github.com/perlin-network/life) Clang-based wasm compiler. Run benchmarks using `./life -polymerase -entry 'method' /path/to/your/wasm/program.wasm`
