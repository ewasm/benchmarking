"""
Copyright 2018 Fluence Labs Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from fluence_bencher.VMDescriptor import VMDescriptor

# export function name that should be called from each Wasm module
test_export_function_name = "main"

"""
    Attributes
    ----------
    vm_relative_binary_path : str
        A relative path to VM binary in its main folder.
    vm_launch_cmd : str
        An format string with command for launch this vm with provided test.

    VMDescriptor(vm_relative_binary_path="", vm_launch_cmd="")
"""

vm_descriptors = {
    "wagon"  : VMDescriptor("wasm-run", "{wasm_file_path}"),
    "wabt"   : VMDescriptor("wabt-wasm-interp", "{wasm_file_path} --run-all-exports"),
    "vanilla-wabt" : VMDescriptor("vanilla-wabt-wasm-interp", "{wasm_file_path} --run-all-exports"),
    "v8-liftoff" : VMDescriptor("node", "--liftoff --no-wasm-tier-up /engines/node/node-timer.js {wasm_file_path}"),
    "v8-turbofan" : VMDescriptor("node", "--no-liftoff /engines/node/node-timer.js {wasm_file_path}"),
    "v8-interpreter" : VMDescriptor("node", "--wasm-interpret-all --liftoff --no-wasm-tier-up /engines/node/node-timer.js {wasm_file_path}"),
    "wasmtime": VMDescriptor("wasmtime", "{wasm_file_path} --invoke=main"),
    "wavm"   : VMDescriptor("wavm-run", "{wasm_file_path} -f {function_name}"),
    "life-polymerase" : VMDescriptor("life", "-polymerase -entry {function_name} {wasm_file_path}"),
    "life"   : VMDescriptor("life", "-entry {function_name} {wasm_file_path}"),
    "wasmi"  : VMDescriptor("invoke", "{wasm_file_path} {function_name}"),
    "asmble" : VMDescriptor("asmble", "invoke -in {wasm_file_path} {function_name} -defmaxmempages 20000"),
    "wamr-interp" : VMDescriptor("iwasm", "-f {function_name} {wasm_file_path}"),
    "wamr-jit" : VMDescriptor("iwasm", "-f {function_name} {wasm_file_path}"),
    "wamr-aot" : VMDescriptor("wamr_aot.sh", "{function_name} {wasm_file_path}"), 
    "wasm3" : VMDescriptor("wasm3", "--func {function_name} {wasm_file_path}"),
    "fizzy" : VMDescriptor("fizzy.sh", "{function_name} {wasm_file_path}"),
    "ssvm"  : VMDescriptor("ssvm", "{wasm_file_path} {function_name}"),
}
