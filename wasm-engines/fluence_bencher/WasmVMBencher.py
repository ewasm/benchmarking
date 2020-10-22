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

from os import listdir
from os.path import join
from time import time
import subprocess
#from subprocess import Popen
from collections import defaultdict
import logging
# TODO: use nanodurationpy because asmble uses nanoseconds
import durationpy
import re
import shlex


class Record:
    """Contains measures of one test launch.

    Attributes
    ----------
    time : time_type
        The execution time of one test.
    cpu_load : int
        The cpu load (in percents) of one test (currently not supported).

    """
    def __init__(self, time=0.0, compile_time=0.0, exec_time=0.0, cpu_load=0):
        self.time = time
        self.compile_time = compile_time
        self.exec_time = exec_time
        self.cpu_load = cpu_load  # TODO


class WasmVMBencher:
    """Launches each VM on given directory on each provided test."""

    def __init__(self, vm_dir="/", error_log="wasm_vm_errors.log"):
        self.vm_dir = vm_dir
        self.enabled_vm = []
        self.logger = logging.getLogger("wasm_bencher_logger")
        self.error_log = error_log

    def log_error(self, error_msg):
        self.logger.info(error_msg)
        print(error_msg, file=open(self.error_log, 'a'))

    def run_tests(self, test_descriptors, vm_bin_path, vm_descriptors):
        """Launches provided tests and returns their execution time.

        Parameters
        ----------
        test_descriptors
            Descriptors of test that should be used for benchmark Wasm VM.
        vm_descriptors
            Descriptors of Wasm VM that should be tested on provided tests.

        Returns
        -------
        {vm : {test_name : [Records]}}
            Collected test results.

       """
        # {vm : {test_name : [Records]}}
        results = defaultdict(lambda: defaultdict(list))

        test_export_function_name = 'main'
        self.enabled_vm = list(vm_descriptors.keys())

        for test_name, test_path in test_descriptors.items():
            self.logger.info("<wasm_bencher>: launch {} test".format(test_name))
            for vm in self.enabled_vm:
                if vm not in vm_descriptors:
                    continue

                # ------------------- TODO don't hardcode the below
                bin_path = "./results/bin"
                vm_binary_full_path = join(vm_descriptors[vm].vm_binary_path)
                cmd = vm_binary_full_path + " " \
                      + vm_descriptors[vm].vm_launch_cmd.format(wasm_file_path=test_path,
                                                                function_name=test_export_function_name)

                # determine repititions for a benchmark by checking the time it takes for one run
                # if its very short, then do many repetitions
                # if > 20 seconds or 30 seconds, then do three repetitions
                try:
                    self.logger.info("<wasm_bencher>: {}".format(cmd))
                    result_record = self.run_engine(vm, cmd)
                    results[vm][test_name].append(result_record)
                    self.logger.info("<wasm_bencher>: {} result collected: time={} compiletime={} exectime={}".format(vm, result_record.time, result_record.compile_time, result_record.exec_time))
                except (subprocess.TimeoutExpired, Exception) as e:
                    self.log_error("<wasm_bencher>: {} ({}) got exception:\n{}".format(vm, cmd, e))
                    self.log_error("<wasm_bencher>: skipping engine {} for bench input {}".format(vm, test_name))
                    continue

                # target 60 seconds total time per benchmark
                repetitions = round(60 / result_record.time)
                if repetitions < 3:
                  repetitions = 3 # minimum
                if repetitions > 50:
                  repetitions = 50 # maximum

                for i in range(repetitions - 1):
                    # run (i+2) of repetitions. 2nd run of 1-based index
                    self.logger.info("<wasm_bencher> {} run {} of {}: {}".format(vm, i + 2, repetitions, cmd))
                    result_record = self.run_engine(vm, cmd)
                    results[vm][test_name].append(result_record)
                    self.logger.info("<wasm_bencher>: {} result collected: time={} compiletime={} exectime={}".format(vm, result_record.time, result_record.compile_time, result_record.exec_time))


        return results

    def run_engine(self, vm, cmd):
        if vm == "lifePolymerase":
            result_record = self.do_life_poly_test(cmd)
        elif vm == "life":
            result_record = self.do_life_test(cmd)
        elif vm == "wavm":
            result_record = self.do_wavm_test(cmd)
        elif vm == "wasmer":
            result_record = self.do_wasmer_test(cmd)
        elif vm == "wasmtime":
            result_record = self.do_wasmtime_test(cmd)
        elif vm == "v8-liftoff" or vm == "v8-turbofan" or vm == "v8-interpreter":
            result_record = self.do_v8_test(cmd)
        elif vm == "asmble":
            result_record = self.do_asmble_test(cmd)
        elif vm == "wagon":
            result_record = self.do_wagon_test(cmd)
        elif vm == "wasmi":
            result_record = self.do_wasmi_test(cmd)
        elif vm == "wabt":
            result_record = self.do_wabt_test(cmd)
        elif vm == "vanilla-wabt":
            result_record = self.do_vanilla_wabt_test(cmd)
        elif vm == "wamr-interp":
            result_record = self.do_wamr_interp_test(cmd)
        elif vm == "wamr-jit":
            result_record = self.do_wamr_jit_test(cmd)
        elif vm == "wamr-aot":
            result_record = self.do_wamr_aot_test(cmd)
        elif vm == "wasm3":
            result_record = self.do_wasm3_test(cmd)
        elif vm == "fizzy":
            result_record = self.do_fizzy_test(cmd)
        elif vm == "ssvm":
            result_record = self.do_ssvm_test(cmd)
        else:
            result_record = self.doElapsedTest(cmd)

        return result_record

    def do_wasmtime_test(self, vm_cmd):
        """
        module compile time: 78.598076ms
        exec time: 73.882µs
        """
        time_parse_info = {
          'compile_line_num' : 0,
          'exec_line_num' : 1,
          'compile_regex': "module compile time: ([\w\.]+)",
          'exec_regex': "exec time: ([\w\.]+)"
        }
        result = self.doCompilerTest(vm_cmd, time_parse_info)
        return Record(time=result.time, compile_time=result.compile_time, exec_time=result.exec_time)

    def do_wasmer_test(self, vm_cmd):
        """02/26/2019 04:43:14 PM <wasm_bencher>: /engines/wasmer-master/target/release/wasmer run /wasmfiles/sha1-42488-bits.wasm                                                                                                              │··············
        compile time: 58.099186ms                                                                                                                                                                                                            │··············
        run time: 54.399µs
        """
        time_parse_info = {
          'compile_line_num' : 0,
          'exec_line_num' : 1,
          'compile_regex': "compile time: ([\w\.]+)",
          'exec_regex': "run time: ([\w\.]+)"
        }
        result = self.doCompilerTest(vm_cmd, time_parse_info)
        return Record(time=result.time, compile_time=result.compile_time, exec_time=result.exec_time)

    def do_wasmer_v014_test(self, vm_cmd):
        """02/15/2019 11:23:55 PM <wasm_bencher>: /engines/wasmer/target/release/wasmer run /wasmfiles/ecpairing.wasm
           compile time: 88.381ms
           total run time (compile + execute): 172.762637ms
           02/15/2019 11:23:55 PM <wasm_bencher>: wasmer result collected: time=0.18068552017211914 compiletime=0.0
        """ 
        # the other wasmer patch prints "run time: 172.762637ms"
        #runtime_match = re.search("run time: ([\w\.]+)", runtime_line)
        time_parse_info = {
          'compile_line_num' : 0,
          'exec_line_num' : 1,
          'compile_regex': "compile time: ([\w\.]+)",
          'exec_regex': "total run time \(compile \+ execute\): ([\w\.]+)"
        }
        result = self.doCompilerTest(vm_cmd, time_parse_info, stderr_redir=False)
        execution_time = result.exec_time - result.compile_time
        return Record(time=result.time, compile_time=result.compile_time, exec_time=execution_time)

    def do_wavm_test(self, vm_cmd):
        """02/16/2019 12:03:32 AM <wasm_bencher>: /engines/wavm-build/bin/wavm-run /wasmfiles/example.wasm -f main
           Object size: 600392                                                                                                                                                                                                                  │··············
           Object size: 800                                                                                                                                                                                                                     │··············
           Instantiation/compile time: 4210686us                                                                                                                                                                                                │··············
           Invoke/run time: 113563us
        """
        # TODO: read wavm compiled object size
        time_parse_info = {
          'compile_line_num' : -2,
          'exec_line_num' : -1,
          'compile_regex': "Instantiation/compile time: ([\w\.]+)",
          'exec_regex': "Invoke/run time: ([\w\.]+)"
        }
        return self.doCompilerTest(vm_cmd, time_parse_info)

    def do_life_test(self, vm_cmd):
        """03/10/2019 05:43:33 AM <wasm_bencher> life run 2 of 12: /engines/life/life -entry main /wasmfiles/bn128_pairing-one_point.wasm
          disasm time: 150.823183ms
          compile time: 194.341499ms
          parse/instantiation time: 348.134957ms
          return value = 0, exec duration = 4.640145939s
        """
        time_parse_info = {
          'compile_line_num' : -2,
          'exec_line_num' : -1,
          'compile_regex': "parse/instantiation time: ([\w\.]+)",
          'exec_regex': "duration = ([\w\.]+)"
        }
        return self.doCompilerTest(vm_cmd, time_parse_info)

    def do_life_poly_test(self, vm_cmd):
        """03/10/2019 12:22:31 AM <wasm_bencher>: /engines/life/life -polymerase -entry main /wasmfiles/bn128_pairing-one_point.wasm
            disasm time: 146.013493ms
            compile time: 208.066141ms
            parse/instantiation time: 357.112707ms
            [Polymerase] Compilation started.
            [Polymerase] Compilation finished successfully in 45.485905579s.
            return value = 0, exec duration = 15.903258ms
        """
        time_parse_info = {
          'compile_line_num' : -2,
          'exec_line_num' : -1,
          'compile_regex': "Compilation finished successfully in ([\w\.]+s).",
          'exec_regex': "duration = ([\w\.]+)"
        }
        return self.doCompilerTest(vm_cmd, time_parse_info)

    def do_v8_test(self, vm_cmd):
        """02/17/2019 07:14:04 PM <wasm_bencher>: /engines/node/node --wasm-interpret-all /engines/node/node-timer.js /wasmfiles/ecpairing.wasm
        args: [ '/wasmfiles/ecpairing.wasm' ]
        ---- reading wasm file..
        ---- wasm file read.
        instantiate: 67.677ms
        ---- calling main...
        run-main: 13406.809ms
        ---- wasm returns: undefined
        """
        time_parse_info = {
          'compile_line_num' : 3,
          'exec_line_num' : 5,
          'compile_regex': "instantiate: ([\w\.]+)",
          'exec_regex': "run-main: ([\w\.]+)"
        }
        return self.doCompilerTest(vm_cmd, time_parse_info)

    def do_wabt_test(self, vm_cmd):
        """02/16/2019 09:56:43 PM <wasm_bencher>: /engines/wabt/bin/wasm-interp /wasmfiles/ecpairing.wasm --run-all-exports
        ec_pairing() => error: argument type mismatch
        main() =>
        parse time: 45430us
        exec time: 62390657us
        """
        time_parse_info = {
          'compile_line_num' : -2,
          'exec_line_num' : -1,
          'compile_regex': "parse time: ([\w]+)",
          'exec_regex': "exec time: ([\w]+)"
        }
        return self.doCompilerTest(vm_cmd, time_parse_info)

    def do_vanilla_wabt_test(self, vm_cmd):
        """02/16/2019 09:56:43 PM <wasm_bencher>: /engines/vanilla-wabt/bin/wasm-interp /wasmfiles/ecpairing.wasm --run-all-exports
        ec_pairing() => error: argument type mismatch
        main() =>
        parse time: 45430us
        exec time: 62390657us
        """
        time_parse_info = {
          'compile_line_num' : -2,
          'exec_line_num' : -1,
          'compile_regex': "parse time: ([\w]+)",
          'exec_regex': "exec time: ([\w]+)"
        }
        return self.doCompilerTest(vm_cmd, time_parse_info)


    def do_wagon_test(self, vm_cmd):
        """03/10/2019 12:14:46 AM <wasm_bencher>: /engines/wagon/cmd/wasm-run/wasm-run /wasmfiles/bn128_pairing-one_point.wasm
        parse time: 1.378798236s
        <nil> (<nil>)
        exec time: 3.972499051s
        """
        time_parse_info = {
          'compile_line_num' : 0,
          'exec_line_num' : -1,
          'compile_regex': "parse time: ([\w\.]+)",
          'exec_regex': "exec time: ([\w\.]+)"
        }
        return self.doCompilerTest(vm_cmd, time_parse_info)

    def do_asmble_test(self, vm_cmd):
        """03/11/2019 01:24:20 PM <wasm_bencher> asmble run 2 of 12: /engines/asmble/bin/asmble invoke -in /wasmfiles/bn128_add-cdetrio11.wasm main -defmaxmempages 20000
        compile time: 4585504732ns
        exec time: 7276335ns
        """
        time_parse_info = {
          'compile_line_num' : 0,
          'exec_line_num' : 1,
          'compile_regex': "compile time: ([\w\.]+)",
          'exec_regex': "exec time: ([\w\.]+)"
        }
        return self.doCompilerTest(vm_cmd, time_parse_info)

    def do_wasmi_test(self, vm_cmd):
        """02/24/2019 05:01:58 PM <wasm_bencher>: /engines/wasmi/target/release/examples/invoke /wasmfiles/sha1-42488-bits.wasm main                                                                                                            │··············
        module parse time: 3.499567ms                                                                                                                                                                                                        │··············
        Result: None                                                                                                                                                                                                                         │··············
        exec time: 4.630356ms
        """
        time_parse_info = {
          'compile_line_num' : 0,
          'exec_line_num' : -1,
          'compile_regex': "module parse time: ([\w\.]+)",
          'exec_regex': "exec time: ([\w\.]+)"
        }
        return self.doCompilerTest(vm_cmd, time_parse_info)

    def do_wamr_interp_test(self, vm_cmd):
        """
        Instantiation time: 0.001776

        execution time: 0.003867
        """
        time_parse_info = {
          'compile_line_num' : 0,
          'exec_line_num' : -1,
          'compile_regex': "Instantiation time: ([\w\.]+)",
          'exec_regex': "execution time: ([\w\.]+)"
        }
        return self.doCompilerTest(vm_cmd, time_parse_info)

    def do_wamr_jit_test(self, vm_cmd):
        """
        Instantiation time: 0.001776

        execution time: 0.003867
        """
        time_parse_info = {
          'compile_line_num' : 0,
          'exec_line_num' : -1,
          'compile_regex': "Instantiation time: ([\w\.]+)",
          'exec_regex': "execution time: ([\w\.]+)"
        }
        return self.doCompilerTest(vm_cmd, time_parse_info)

    def do_wamr_aot_test(self, vm_cmd):
        """
        engine output:
        Runtime load time: 0.000205s
        Create AoT compiler with:
          target:        x86_64
          target cpu:    broadwell
          cpu features:  
          opt level:     3
          size level:    3
          output format: AoT file
        Compilation time: 0.002127s
        Compile success, file wasm.aot was generated.
        Instantiation time: 0.000860s
        Exception: invalid input argument count.
        execution time: 0.000001s
        """
        time_parse_info = {
          'compile_line_num' : 8,
          'exec_line_num' : -1,
          'compile_regex': "Compilation time: ([\w\.]+)",
          'exec_regex': "execution time: ([\w\.]+)"
        }
        return self.doCompilerTest(vm_cmd, time_parse_info)



    def do_wasm3_test(self, vm_cmd):
        """
        Result: <Empty Stack>
        Instantiation time: 0.000046
        execution time: 0.001948
        """

        time_parse_info = {
          'compile_line_num' : 1,
          'exec_line_num' : -1,
          'compile_regex' : "Instantiation time: ([\w\.]+)",
          'exec_regex' : "execution time: ([\w\.]+)"
        }
        return self.doCompilerTest(vm_cmd, time_parse_info)

    def do_fizzy_test(self, vm_cmd):
        """
        2020-02-26 03:37:35
        Running /engines/fizzy/build/bin/fizzy-bench
        Run on (4 X 3100 MHz CPU s)
        CPU Caches:
          L1 Data 32K (x2)
          L1 Instruction 32K (x2)
          L2 Unified 256K (x2)
          L3 Unified 3072K (x1)
        Load Average: 0.54, 0.65, 0.76
        ***WARNING*** CPU scaling is enabled, the benchmark real time measurements may be noisy and will incur extra overhead.
        --------------------------------------------------------------------------------------
        Benchmark                            Time             CPU   Iterations UserCounters...
        --------------------------------------------------------------------------------------
        fizzy/parse/testcase            159223ns       158598ns         4375 rate=1.50602G/s size=238.852k
        fizzy/instantiate/testcase       30759ns        30557ns        23588
        fizzy/execute/testcase/test    2274841ns      2263767ns          315
        """

        time_parse_info = {
                'compile_line_num' : -2,
                'exec_line_num' : -1,
                'compile_regex' : "fizzy\/instantiate\/testcase\s+([0-9]+ *[a-z]+)",
                'exec_regex': "fizzy\/execute\/testcase\/test\s+([0-9]+ *[a-z]+)"
        }
        return self.doCompilerTest(vm_cmd, time_parse_info)

    def do_ssvm_test(self, vm_cmd):
        """
        Instantiation time: 0.003753s
        2020-04-22 13:49:02,940 DEBUG [default] [user@fe598b959cdc] [SSVM::Expect<void> SSVM::Interpreter::Interpreter::runFunction(SSVM::Runtime::StoreManager&, const SSVM::Run
        time::Instance::FunctionInstance&)] [/engines/SSVM/lib/interpreter/engine/engine.cpp:33] Start running...
        2020-04-22 13:49:02,945 DEBUG [default] [user@fe598b959cdc] [SSVM::Expect<void> SSVM::Interpreter::Interpreter::runFunction(SSVM::Runtime::StoreManager&, const SSVM::Run
        time::Instance::FunctionInstance&)] [/engines/SSVM/lib/interpreter/engine/engine.cpp:36] Execution succeeded.
        2020-04-22 13:49:02,945 DEBUG [default] [user@fe598b959cdc] [SSVM::Expect<void> SSVM::Interpreter::Interpreter::runFunction(SSVM::Runtime::StoreManager&, const SSVM::Run
        time::Instance::FunctionInstance&)] [/engines/SSVM/lib/interpreter/engine/engine.cpp:44] Done.
        2020-04-22 13:49:02,945 DEBUG [default] [user@fe598b959cdc] [SSVM::Expect<void> SSVM::Interpreter::Interpreter::runFunction(SSVM::Runtime::StoreManager&, const SSVM::Run
        time::Instance::FunctionInstance&)] [/engines/SSVM/lib/interpreter/engine/engine.cpp:52] 
        =================  Statistics  =================
        Total execution time: 4448us
        Wasm instructions execution time: 4448us
        Host functions execution time: 0us
        Executed wasm instructions count: 137054
        Gas costs: 137054
        Instructions per second: 30812500
        """
        time_parse_info = {
            'compile_line_num': 0,
            'exec_line_num': -6,
            'compile_regex' : "Instantiation time: ([\w\.]+)",
            'exec_regex' : "Total execution time: ([\w\.]+)"
        }
        return self.doCompilerTest(vm_cmd, time_parse_info)

    def doElapsedTest(self, vm_cmd):
        """Launches provided shell command string via subprocess.Popen and measure its execution time.

        Parameters
        ----------
        vm_cmd : str
            An exactly command that should be executed.

        Returns
        -------
        time_type
            An elapsed time of provided cmd execution.

        """
        start_time = time()
        #Popen(vm_cmd, shell=True).wait(300)
        cmd_args = shlex.split(vm_cmd)
        vm_process = subprocess.run(cmd_args, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, timeout=300)
        end_time = time()
        #stdoutlines = [str(line, 'utf8') for line in vm_process.stdout]
        stdoutlines = [line for line in vm_process.stdout.decode('utf8').rstrip().split('\n')]
        print(("\n").join(stdoutlines), end="\n")
        return Record(end_time - start_time)

    def doCompilerTest(self, vm_cmd, time_parse_info, stderr_redir=True):
        start_time = time()
        cmd_args = shlex.split(vm_cmd)
        print(cmd_args)
        if stderr_redir:
            vm_process = subprocess.run(cmd_args, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, timeout=300)
        else:
            vm_process = subprocess.run(cmd_args, stdout=subprocess.PIPE, shell=True, timeout=300)
        #vm_process.wait(300)
        end_time = time()
        total_time = end_time - start_time
        #stdoutlines = [str(line, 'utf8') for line in vm_process.stdout]
        stdoutlines = [line for line in vm_process.stdout.decode('utf8').rstrip().split('\n')]
        print('stdout_lines: ', ("\n").join(stdoutlines), end="\n")
        try:
            compile_line = stdoutlines[time_parse_info['compile_line_num']]
            print('compile_lines: ', compile_line)
            compile_match = re.search(time_parse_info['compile_regex'], compile_line)
            compile_match = compile_match[1].replace(' ', '')
            print('compile_match: ', compile_match)
            compile_time = durationpy.from_str(compile_match)
            print('compile_time: ', compile_time)

            exec_line = stdoutlines[time_parse_info['exec_line_num']]
            print('exec_line: ', exec_line)
            exec_match = re.search(time_parse_info['exec_regex'], exec_line)
            exec_match = exec_match[1].replace(' ', '')
            print('exec_match: ', exec_match)
            exec_time = durationpy.from_str(exec_match)
            print('exec_time: ', exec_time)
        except Exception as e:
            error_msg = ["Error parsing engine output. exception: {}".format(e)] + \
                        ["engine output:"] + stdoutlines
            raise Exception("\n".join(error_msg))
        return Record(time=total_time, compile_time=compile_time.total_seconds(), exec_time=exec_time.total_seconds())

