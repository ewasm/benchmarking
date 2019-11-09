#!/usr/bin/python3

import csv

RESULT_CSV_OUTPUT_PATH = "/evmraceresults/"
EVMS = ["evmone", "parity", "geth", "cita-vm"]
RESULT_FILE = "evm_benchmarks.csv"

def main():
    fieldnames = ['engine', 'test_name', 'total_time', 'gas_used']
    evm_results = []
    merged_data = []
    
    for evm in EVMS:
        path = RESULT_CSV_OUTPUT_PATH + "evm_benchmarks_" + evm + ".csv"
        data_file = open(path, 'r')
        data = data_file.read().splitlines()
        data_file.close()
        evm_results.append(data)
        

    with open(RESULT_FILE, 'w', newline='') as bench_result_file:
        writer = csv.DictWriter(bench_result_file, fieldnames=fieldnames)
        writer.writeheader()

    for i in range(0, len(evm_results[0])):
        for e in range(0, len(EVMS)):
            if i == 0:  # skip header
                continue
            merged_data.append(evm_results[e][i])

    with open(RESULT_FILE, 'a', newline='') as bench_result_file:
        for line in merged_data:
            bench_result_file.write(line)
            

if __name__ == "__main__":
    main()
