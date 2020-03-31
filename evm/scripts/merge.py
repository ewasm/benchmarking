#!/usr/bin/python3

import csv
import os

RESULT_CSV_OUTPUT_PATH = "/evmraceresults/"
EVMS = ["evmone", "parity", "geth", "cita-vm"]
RESULT_FILE = os.path.join(RESULT_CSV_OUTPUT_PATH + "evm_benchmarks.csv")

# translate a string representing a numerical field like '1.8M' to '1800000'
def format_evmone_benchmark(csv_line):
    fields = csv_line.split(',')
    gas_used = fields[-1]

    if gas_used[-1].lower() == 'k':
        gas_used = str(int(float(gas_used[:-1]) * 1000))
    elif gas_used[-1].lower() == 'm':
        gas_used = str(int(float(gas_used[:-1]) * 1000000))
    else:
        return csv_line

    return ','.join(fields[:-1] + [gas_used])[:-1]

# merge benchmarks from multiple engines into one csv output
def main():
    merged_csv_contents = 'engine, test_name, total_time, gas_used\n'
    evm_results = []
    
    for evm in EVMS:
        path = RESULT_CSV_OUTPUT_PATH + "evm_benchmarks_" + evm + ".csv"
        data_file = open(path, 'r')
        data = data_file.read().splitlines()
        data_file.close()
        evm_results.append(data)
        
    for i in range(1, len(evm_results[0])):
        for e in range(0, len(EVMS)):
            if EVMS[e] == 'evmone':
                merged_csv_contents += format_evmone_benchmark(evm_results[e][i]) + '\n'
            else:
                merged_csv_contents += evm_results[e][i] + '\n'

    with open(RESULT_FILE, 'w') as bench_result_file:
        bench_result_file.write(merged_csv_contents)
            

if __name__ == "__main__":
    main()
