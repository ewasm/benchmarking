all: build_docker_images benchmark generate_charts 

build_evm_engines:
	cd evm/geth && docker build . -t ewasm/geth-bench:1
	cd evm/parity && docker build . -t ewasm/parity-bench:1
	cd evm/evmone && docker build . -t ewasm/evmone-bench:1
	cd evm/cita-vm && docker build . -t ewasm/cita-vm-bench:1
	cd evm/evmone-evm384 && docker build . -t ewasm/evmone-evm384-bench:1

build_wasm_engines:
	cd wasm-engines && ./build_engines.sh

build_scout_engines:
	cd scout-engines && docker build . -t ewasm/scout-engines:1

build_docker_images: build_evm_engines build_wasm_engines build_scout_engines

benchmark_evm_engines:
	cd evm && \
	./scripts/run_bench.sh

benchmark_scout_engines:
	cd scout-engines && \
	./run_benchmarks.sh && \
	cp benchmarks_results_data/scout_bignum_benchmarks.csv ../benchmark_results_data/

benchmark_wasm_engines:
	cd wasm-engines && \
	./run_benchmarks.sh && \
	cp benchmark_results_data/standalone_wasm_results.csv ../benchmark_results_data/ && \
	cp benchmark_results/data/native_results.csv ../benchmark_results_data/

benchmark: benchmark_scout_engines benchmark_wasm_engines benchmark_evm_engines benchmark_evm_precompiles

generate_charts:
	cd charts && \
	python3 generate-charts.py
