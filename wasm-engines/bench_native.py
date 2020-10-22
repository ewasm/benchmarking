def bench_rust_binary(rustdir, input_name, native_exec):
    print("running rust native {}...\n{}".format(input_name, native_exec))
    bench_times = []
    for i in range(1,RUST_BENCH_REPEATS):
        rust_process = subprocess.Popen(native_exec, cwd=rustdir, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
        rust_process.wait(None)
        stdoutlines = [str(line, 'utf8') for line in rust_process.stdout]
        print(("").join(stdoutlines), end="")
        elapsedline = stdoutlines[0]
        elapsedmatch = re.search("Time elapsed in bench\(\) is: ([\w\.]+)", elapsedline)
        elapsed_time = durationpy.from_str(elapsedmatch[1])
        bench_times.append(elapsed_time.total_seconds())
    return bench_times

def do_rust_bench(benchname, input, rust_code_dir, wasm_out_dir):
    #rustsrc = "{}/rust-code/src/bench.rs".format(os.path.abspath(benchname))
    #rustsrc = "{}/rust-code".format(os.path.abspath(benchname))
    rust_code_path = os.path.abspath(os.path.join(rust_code_dir, benchname))
    #rustsrc = "{}/rust-code".format(os.path.abspath(benchname))
    rustsrc = rust_code_path
    #rusttemplate = "{}/src/bench.rs".format(rustsrc)
    rusttemplate = os.path.join(rust_code_path, "src/bench.rs")

    if not os.path.exists(rustsrc):
        return False

    #filldir = os.path.abspath("{}/rust-code-filled".format(benchname))
    filldir = os.path.abspath(os.path.join("./rust-code-filled/", benchname))
    if os.path.exists(filldir):
        shutil.rmtree(filldir)
    shutil.copytree(rustsrc, filldir)

    template_args = {}
    for key in input.keys():
        if key == "name":
            continue
        if key == "input":
            input_len = int(len(input['input']) / 2)
            input_str = "let input: [u8; {}] = {};".format(input_len, get_rust_bytes(input['input']))
            template_args["input"] = input_str
        elif key == "expected":
            expected_len = int(len(input['expected']) / 2)
            expected_str = "let expected: [u8; {}] = {};".format(expected_len, get_rust_bytes(input['expected']))
            template_args["expected"] = expected_str
        else:
            template_args[key] = input[key]

    # fill template if necessary
    if len(template_args.keys()) > 1:
        print("filling template for {}".format(input['name']))
        with open(rusttemplate) as file_:
            template = jinja2.Template(file_.read())
            filledrust = template.render(**template_args)

        #rustfileout = "{}/src/bench.rs".format(filldir)
        rustfileout = os.path.join(filldir, "src/bench.rs")
        with open(rustfileout, 'w') as outfile:
            outfile.write(filledrust)

    # compile rust code
    benchname_rust = benchname.replace("-", "_")
    rust_native_cmd = "cargo build --release --bin {}_native".format(benchname_rust)
    print("compiling rust native {}...\n{}".format(input['name'], rust_native_cmd))
    rust_process = subprocess.Popen(rust_native_cmd, cwd=filldir, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    return_code = rust_process.wait(None)
    stdoutlines = [str(line, 'utf8') for line in rust_process.stdout]
    print(("").join(stdoutlines), end="")

    if return_code != 0:
        sys.exit(-1)

    # native binary is at ./target/release/sha1_native
    exec_path = "{}/target/release/{}_native".format(filldir, benchname_rust)
    exec_size = os.path.getsize(exec_path)

    # TODO: get rustc compile time
    # TODO: also build with optimization turned off

    # TODO: run wasm through wasm-gc
    rust_wasm_cmd = "cargo build --release --lib --target wasm32-unknown-unknown"
    print("compiling rust wasm {}...\n{}".format(input['name'], rust_wasm_cmd))
    rust_process = subprocess.Popen(rust_wasm_cmd, cwd=filldir, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
    return_code = rust_process.wait(None)
    stdoutlines = [str(line, 'utf8') for line in rust_process.stdout]
    print(("").join(stdoutlines), end="")
    if return_code != 0:
        sys.exit(-1)
    # wasm is at ./target/wasm32-unknown-unkown/release/sha1_wasm.wasm
    wasmbin = "{}/target/wasm32-unknown-unknown/release/{}_wasm.wasm".format(filldir, benchname_rust)
    wasmdir = os.path.abspath(wasm_out_dir)
    wasmoutfile = os.path.join(wasmdir, "{}.wasm".format(input['name']))
    if not os.path.exists(wasmdir):
        os.mkdir(wasmdir)
    shutil.copy(wasmbin, wasmoutfile)

    # TODO: get cargo build compiler time and report along with exec time.

    # run rust binary

def main():
    pass

if __name__ == "__main__":
    main()
