all: evm_precompiles evm_engines wasm_engines scout_engines notebook

build_docker_images:
	cd evm/geth && docker build . -t geth-bench
	cd evm/parity && docker build . -t parity-bench
	cd evm/evmone && docker build . -t evmone-bench
	cd evm/cita-vm && docker build . -t cita-vm-bench
	cd evm/evmone-evm384 && docker build . -t evmone-evm384-bench
	cd wasm-engines && ./build_engines.sh
	cd scout-engines && docker build . -t scout-engines

evm_precompiles: build_docker_images
	cd evm && ./scripts/run_precompiles_bench.sh geth
	cd evm && ./scripts/run_precompiles_bench.sh parity

evm_engines: build_docker_images
	cd evm && ./scripts/run_bench.sh

scout_engines: build_docker_images
	cd scout-engines && ./run_benchmarks.sh

wasm_engines:
	docker pull ewasm/bench:1
	cd wasm-engines && ./run_benchmarks.sh

# Default timeout is 30 seconds, but our cells are quite big, increase it to 120 seconds.
# More info: https://github.com/jupyter/nbconvert/issues/256#issuecomment-188405852
# TODO: upgrade to newer nbconvert which sets the timeout to off by default
notebook:
	cd notebooks && jupyter nbconvert --execute --ExecutePreprocessor.timeout=120 --to notebook --inplace wasm-engines.ipynb
