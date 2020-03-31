#!/usr/bin/python3

import csv
import os

RESULT_CSV_OUTPUT_PATH = "/evmraceresults/"
EVMS = ["evmone", "parity", "geth", "cita-vm"]
RESULT_FILE = os.path.join(RESULT_CSV_OUTPUT_PATH + "evm_benchmarks.csv")

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
            merged_csv_contents += evm_results[e][i] + '\n'

    with open(RESULT_FILE, 'w') as bench_result_file:
        bench_result_file.write(merged_csv_contents)
            

if __name__ == "__main__":
    main()
