#! /bin/bash

docker run --privileged \
	-v $(pwd)/fluence_bencher:/benchrunner/fluence_bencher \
	-v $(pwd)/main.py:/benchrunner/main.py \
	-v $(pwd)/benchnativerust_prepwasm.py:/benchprep/benchnativerust_prepwasm.py \
	-v $(pwd)/wasmfiles:/wasmfiles \
	-v $(pwd)/benchmark_results_data:/benchmark_results_data \
	-v $(pwd)/nanodurationpy.py:/benchprep/nanodurationpy.py \
	-v $(pwd)/rust-code:/benchprep/rust-code \
	-v $(pwd)/inputvectors:/benchprep/inputvectors \
	-v $(pwd)/benchmeteredstandalone.sh:/benchprep/benchmeteredstandalone.sh \
	-v $(pwd)/bench_wasm_and_native.sh:/benchprep/bench_wasm_and_native.sh \
	-v $(pwd)/node-timer.js:/engines/node/node-timer.js \
	-v $(pwd)/wamr_aot.sh:/engines/wamr/wamr_aot.sh \
	-v $(pwd)/fizzy.sh:/engines/fizzy/fizzy.sh \
--security-opt seccomp=$(pwd)/dockerseccompprofile.json -it ewasm/wasm-engines-bench:1 bash /benchprep/bench_wasm_and_native.sh
