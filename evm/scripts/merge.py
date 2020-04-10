#!/usr/bin/python3

import csv
import os
import time
import datetime
import shutil

INDIVIDUAL_EVM_RESULTS_CSV_PATH = "/evmraceresults/"
RESULT_CSV_OUTPUT_PATH = "/benchmark_results_data/"
EVMS = ["evmone", "parity", "geth", "cita-vm"]
RESULT_CSV_FILENAME = "evm_benchmarks.csv"
RESULT_FILE = os.path.join(RESULT_CSV_OUTPUT_PATH, RESULT_CSV_FILENAME)

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
        path = os.path.join(INDIVIDUAL_EVM_RESULTS_CSV_PATH, "evm_benchmarks_{}.csv".format(evm))
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


    # move existing csv file to backup-datetime-folder
    ts = time.time()
    date_str = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    ts_folder_name = "backup-{}-{}".format(date_str, round(ts))
    dest_backup_path = os.path.join(RESULT_CSV_OUTPUT_PATH, ts_folder_name)

    # back up existing result csv file
    if os.path.isfile(RESULT_FILE):
        os.makedirs(dest_backup_path)
        shutil.move(RESULT_FILE, dest_backup_path)
        print("existing {} moved to {}".format(RESULT_CSV_FILENAME, dest_backup_path))

    with open(RESULT_FILE, 'w') as bench_result_file:
        bench_result_file.write(merged_csv_contents)

    print("saved evm results to:", RESULT_FILE)


if __name__ == "__main__":
    main()
