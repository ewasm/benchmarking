import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np
import durationpy
import math

from os.path import join
from plot_util import *
from adjustText import adjust_text

#############
# CONSTANTS #
#############

if __name__ == "__main__":
# csv result files directory name and file names
    CSV_RESULT_DIR = "../benchmark_results_data"
    WASM_RESULT_FILE = "standalone_wasm_results.csv"
    NATIVE_RESULT_FILE = "native_benchmarks.csv"
    SCOUT_RESULT_FILE = "scout_bignum_benchmarks.csv"


# To add a new engine, add the engine name used in the csv file to the list
    INTERPRETER_ENGINES = ['life', 'wagon', 'wasmi', 'wabt', 'v8-interpreter', 'wasm3', 'wamr', 'fizzy']
    COMPILER_ENGINES = ['lifePolymerase', 'wasmtime', 'wavm', 'v8-liftoff', 'v8-turbofan', 'asmble']

    wasm_vm_names = INTERPRETER_ENGINES + COMPILER_ENGINES

    # print('CPU Information')
    # with open(join(CSV_RESULT_DIR, "cpuinfo.txt"), 'r') as cpuinfofile:
    #     [print(line.rstrip()) for line in cpuinfofile.readlines()]


#########
# SCOUT #
#########

# Import scout engine results
    df_scout_data = read_results(join(CSV_RESULT_DIR, SCOUT_RESULT_FILE))


# Compare wabt-optimized against wabt-baseline on hash function benchmark


# Plot biturbo benchmark:
# biturbo-token-eth1-mainnet-stateless-block-hexary-trie-keccac256-multiproof
    df_scout_biturbo_token = df_scout_data[df_scout_data['bench_name'] == 'biturbo-token-eth1-mainnet-stateless-block-hexary-trie-keccak256-multiproof']

    df_scout_means_biturbo_token = df_scout_biturbo_token.groupby(['engine']).mean()
    df_scout_fast_biturbo_token = filterDfEngines(df_scout_biturbo_token, ['v8-interpreter'])
    df_scout_fast_biturbo_means = df_scout_fast_biturbo_token.groupby(['engine']).mean()



# Plot bignum benchmark:
# ecrecover-eth1-txns-websnark-secp256k1-verify-72-sigs
    df_scout_ecrecover_websnark_secp256k1 = df_scout_data[df_scout_data['bench_name'] == 'ecrecover-eth1-txns-websnark-secp256k1-verify-72-sigs']

    df_scout_means_ecrecover_websnark_secp256k1 = df_scout_ecrecover_websnark_secp256k1.groupby(['engine']).mean()
    df_scout_fast_ecrecover = filterDfEngines(df_scout_ecrecover_websnark_secp256k1,
        ['v8-interpreter', 'scoutcpp-wabt-no-bignums', 'wabt-no-bignums'])
    df_scout_fast_ecrecover_means = df_scout_fast_ecrecover.groupby(['engine']).mean()



# Plot bignum benhmark:
# ecpairing-zkrollup-websnark-bn128-two-pairings
    df_scout_ecpairing_zkrollup_bn128_pairings = df_scout_data[df_scout_data['bench_name'] == 'ecpairing-zkrollup-websnark-bn128-two-pairings']

    df_scout_means_ecpairing_zkrollup = df_scout_ecpairing_zkrollup_bn128_pairings.groupby(['engine']).mean()
    df_scout_fast_ecpairing_zkrollup = filterDfEngines(df_scout_ecpairing_zkrollup_bn128_pairings,
        ['v8-interpreter', 'scoutcpp-wabt-no-bignums', 'wabt-no-bignums'])
    df_scout_fast_means_ecpairing_zkrollup = df_scout_fast_ecpairing_zkrollup.groupby(['engine']).mean()



# Plot bignum benchmark:
# daiquiri-zkmixer-websnark-bn128-groth16-four-pairings-and-mimc
    df_scout_daiquiri_zkmixer = df_scout_data[df_scout_data['bench_name'] == 'daiquiri-zkmixer-websnark-bn128-groth16-four-pairings-and-mimc']

    df_scout_means_daiquiri_zkmixer = df_scout_daiquiri_zkmixer.groupby(['engine']).mean()
    df_scout_fast_daiquiri_zkmixer = filterDfEngines(df_scout_daiquiri_zkmixer,
        ['v8-interpreter', 'scoutcpp-wabt-no-bignums', 'wabt-no-bignums'])
    df_scout_fast_means_daiquiri_zkmixer = df_scout_fast_daiquiri_zkmixer.groupby(['engine']).mean()



###########################
# Wasm Engines Benchmarks #
###########################

# Import wasm results
    df_wasm = read_results(join(CSV_RESULT_DIR, WASM_RESULT_FILE))

# Import native results
    df_native_raw = read_results(join(CSV_RESULT_DIR, NATIVE_RESULT_FILE))


    native_results = {}
    for i in range(len(df_native_raw)):
        test_name = df_native_raw['test_name'][i]
        native_results[test_name] = df_native_raw['elapsed_times'][i].split(', ')

    test_names = df_native_raw['test_name'].tolist()

    native_times = {}
    for test in test_names:
        avg = np.mean([float(t) for t in native_results[test]])
        native_times[test] = avg
        
    df_native = pd.DataFrame.from_dict(native_times, orient='index', columns=['elapsed_time'])
    df_native['engine'] = 'rust-native'

# Sorted list of test names for plotting inputs in order
    blake2b_test_names = [name for name in df_wasm['test_name'].unique().tolist() if 'blake2b' in name]
    blake2b_test_names.sort()
    blake2b_test_names_desc = blake2b_test_names.copy()
    blake2b_test_names_desc.reverse()


    sha1_test_names = [name for name in df_wasm['test_name'].unique().tolist() if 'sha1' in name]
    sha1_test_names.sort()
    sha1_test_names_desc = sha1_test_names.copy()
    sha1_test_names_desc.reverse()


    bn128_mul_test_names = ['bn128_mul-cdetrio11', 'bn128_mul-chfast2', 'bn128_mul-chfast1']
    bn128_add_test_names = ['bn128_add-cdetrio11', 'bn128_add-cdetrio14', 'bn128_add-cdetrio10']
    bn128_pairing_test_names = ['bn128_pairing-ten_point_match_1', 'bn128_pairing-two_point_match_2', 'bn128_pairing-one_point']

    bn128_mul_test_names.reverse()
    bn128_add_test_names.reverse()
    bn128_pairing_test_names.reverse()

    bn128_mul_test_names_desc = ['bn128_mul-cdetrio11', 'bn128_mul-chfast2', 'bn128_mul-chfast1']
    bn128_add_test_names_desc = ['bn128_add-cdetrio11', 'bn128_add-cdetrio14', 'bn128_add-cdetrio10']
    bn128_pairing_test_names_desc = ['bn128_pairing-ten_point_match_1', 'bn128_pairing-two_point_match_2', 'bn128_pairing-one_point']

    bls12_test_names = ['bls12-381-aggreg-32-pubkeys-verify-sig', 'bls12-381-aggreg-64-pubkeys-verify-sig', 'bls12-381-aggreg-128-pubkeys-verify-sig']
    bls12_test_names_desc = bls12_test_names.copy()
    bls12_test_names_desc.reverse()

    modexp_test_names = [name for name in df_wasm['test_name'].unique().tolist() if 'modexp' in name]
    modexp_test_names.sort()
    modexp_test_names_desc = modexp_test_names.copy()
    modexp_test_names_desc.reverse()

    all_tests = sha1_test_names + blake2b_test_names + modexp_test_names + ['ed25519-verify-ten-inputs'] + bls12_test_names \
        + bn128_add_test_names + bn128_mul_test_names + bn128_pairing_test_names

# Prepare interpreter dataframe
    all_interp_test_names = []

    interp_results_for_df = []
    for engine in INTERPRETER_ENGINES:
        df_engine = df_wasm[df_wasm['engine'] == engine]
        df_means = df_engine.groupby(['test_name']).mean()
        test_names = df_engine['test_name'].unique().tolist()
        all_interp_test_names.extend(test_names)
        for test_name in test_names:
            interp_results_for_df.append([engine, test_name] + df_means.loc[test_name].tolist())

    all_interp_test_names = set(all_interp_test_names)

    df_interp = pd.DataFrame(interp_results_for_df)
    df_interp.columns = ['engine', 'test_name', 'elapsed_time', 'parse_time', 'exec_time']
    df_interp.set_index('engine', inplace=True)
    df_interp['total_time'] = df_interp['parse_time'] + df_interp['exec_time']








# Chart of only the fast interpreters


####################
# Compiler Results #
####################

# Prepare compilers dataframe
    compiler_results_for_df = []
    for engine in COMPILER_ENGINES:
        df_engine = df_wasm[df_wasm['engine'] == engine]
        df_means = df_engine.groupby(['test_name']).mean()
        test_names = df_engine['test_name'].unique().tolist()
        for test_name in test_names:
            compiler_results_for_df.append([engine, test_name] + df_means.loc[test_name].tolist())

    df_compiler = pd.DataFrame(compiler_results_for_df)
    df_compiler.columns = ['engine', 'test_name', 'elapsed_time', 'compile_time', 'exec_time']
    df_compiler.set_index('engine', inplace=True)
    df_compiler['total_time'] = df_compiler['compile_time'] + df_compiler['exec_time']






# Add rust-native to compiler engines chart

# merge df_native and df_compiler into one dataframe
# both dataframes must have same columns to merge them:
# engine, test_name, elapsed_time, compile_time, exec_time, total_time

    df_native_merge = df_native.copy()
    df_native_merge.reset_index(inplace=True)
    df_native_merge.columns = ['test_name', 'elapsed_time', 'engine']
    df_native_merge['compile_time'] = 0
    df_native_merge['exec_time'] = df_native_merge['elapsed_time']
    df_native_merge['total_time'] = df_native_merge['elapsed_time']
    df_native_and_compile = pd.concat([df_compiler.reset_index(), df_native_merge], sort=False)
    df_native_and_compile.reset_index(drop=True, inplace=True)
    df_native_and_compile.set_index('engine', inplace=True)



###################################
# Interpreter vs Compiler speedup #
###################################

# merge df_compiler and df_interp
    df_interp_merge = df_interp.copy()
    df_interp_merge.columns = ['test_name', 'elapsed_time', 'compile_time', 'exec_time', 'total_time']
    df_interp_and_compile = pd.concat([df_interp_merge, df_compiler])
    df_interp_and_compile = df_interp_and_compile.reset_index()



    df_wabt_v8liftoff = add_engine_ratio_col(df_interp_and_compile, "wabt", "v8-liftoff")
    df_fizzy_v8liftoff = add_engine_ratio_col(df_interp_and_compile, "fizzy", "v8-liftoff")
    df_wasm3_v8liftoff = add_engine_ratio_col(df_interp_and_compile, "wasm3", "v8-liftoff")
    df_wasmi_wavm = add_engine_ratio_col(df_interp_and_compile, "wasmi", "wavm")


# import pdb; pdb.set_trace()


########################################################
# All precompiles compared (are interpreters feasible? #
########################################################




# plotOneTestColoredTicks(df_scout_means_rolluprs,
#             suptitle="rollup.rs-bn128-pairings - fast Scout engines (v8-liftoff and wabt-with-bignums)",
#             suptitle_pos=1.02,
#             subtitle="ecpairing-zkrollup-rust-wasm-bn128-two-pairings\n",
#             subtitle_size='xx-large',
#             highlight_tick="wabt-with-bignums")

    only_plot_new_bn = True

    if not only_plot_new_bn:
        plotThreeTestsGrouped(df_scout_data, ["blake2b_64", "blake2b_256", "blake2b_1024"], "blake2b C implementations compared")
        plotThreeTestsGrouped(df_scout_data, ["sha256_64", "sha256_256", "sha256_1024"], "sha256 C implementations compared")
        plotThreeTestsGrouped(df_scout_data, ["keccak256_64", "keccak256_256", "keccak256_1024"], "keccak256 C implementations compared")
        plotOneTest(df_scout_means_biturbo_token,
                    suptitle="\nbiturbo token - all scout engines",
                    suptitle_pos=1.05,
                    subtitle="biturbo-token-eth1-mainnet-stateless-block-hexary-trie-keccak256-multiproof\n",
                    subtitle_size='xx-large')

        plotScoutStackedTest(df_scout_fast_biturbo_means,
                    suptitle="\nbiturbo token - fast scout engines - wasm compilers vs interpreters (v8 vs wabt)",
                    suptitle_pos=1.03,
                    subtitle="biturbo-token-eth1-mainnet-stateless-block-hexary-trie-keccak256-multiproof\n",
                    subtitle_size='xx-large')
        plotOneTest(df_scout_means_ecrecover_websnark_secp256k1,
                    suptitle="websnark-secp256k1-sig-verify - all Scout engines",
                    suptitle_pos=1.0,
                    subtitle="ecrecover-eth1-txns-websnark-secp256k1-verify-72-sigs\n",
                    subtitle_size='xx-large')

        plotScoutStackedTest(df_scout_fast_ecrecover_means,
                    #suptitle="websnark-secp256k1-sig-verify - fast Scout engines - compilers (v8) vs interpreters (wabt)",
                    suptitle="compiler engines - optimizing (v8-turbofan) and single-pass (v8-liftoff) \n vs. \n interpreter engine (wabt) with bignum host funcs",
                    suptitle_pos=1.07,
                    subtitle="ecrecover-eth1-txns-websnark-secp256k1-verify-72-sigs\n",
                    subtitle_size='xx-large')
        plotOneTest(df_scout_means_ecpairing_zkrollup,
                    suptitle="websnark-bn128-pairings - all Scout engines",
                    suptitle_pos=1.02,
                    subtitle="ecpairing-zkrollup-websnark-bn128-two-pairings\n",
                    subtitle_size='xx-large')

        plotScoutStackedTest(df_scout_fast_means_ecpairing_zkrollup,
                    suptitle="compiler engines - optimizing (v8-turbofan) and single-pass (v8-liftoff) \n vs. \n interpreter engine (wabt) with bignum host funcs",
                    suptitle_pos=1.07,
                    subtitle="ecpairing-zkrollup-websnark-bn128-two-pairings\n",
                    subtitle_size='xx-large')
        plotOneTest(df_scout_means_daiquiri_zkmixer,
                    suptitle="daiquiri-zkmixer - all Scout engines",
                    suptitle_pos=1.02,
                    subtitle="daiquiri-zkmixer-websnark-bn128-groth16-four-pairings-and-mimc\n",
                    subtitle_size='xx-large')

        plotScoutStackedTest(df_scout_fast_means_daiquiri_zkmixer,
                    suptitle="wasm compilers - optimizing (v8-turbofan) and single-pass (v8-liftoff) \n vs. \n wasm interpreter (wabt) with bignum host funcs",
                    suptitle_pos=1.07,
                    subtitle="daiquiri-zkmixer-websnark-bn128-groth16-four-pairings-and-mimc\n",
                    subtitle_size='xx-large')
        plotInterpThreeTests(df_interp, blake2b_test_names, title="wasm interpreters compared - blake2b")
        plotInterpThreeTests(df_interp,
                             blake2b_test_names,
                             title="wasm interpreters compared - blake2b")

        plotInterpThreeTests(df_interp,
                             modexp_test_names,
                             title="wasm interpreters compared - modexp")

        plotInterpThreeTests(df_interp,
                             bn128_add_test_names,
                             title="wasm interpreters compared - bn128_add")

        plotThreeTestsExecTime(df_interp, blake2b_test_names, title="wasm interpreter execution time - blake2b")

        plotThreeTestsExecTime(df_interp,
                               modexp_test_names,
                               title="wasm interpreter execution time - modexp")

        plotThreeTestsExecTime(df_interp,
                               bn128_mul_test_names,
                               title="wasm interpreter execution time - bn128_mul")

        plotThreeTestsExecTime(df_interp,
                               bn128_pairing_test_names,
                               title="wasm interpreter execution time - bn128_pairing")
        plotCompilerSpeedup(df_wabt_v8liftoff, all_tests, interp_name="wabt", compiler_name="v8-liftoff")
        plotCompilerSpeedup(df_fizzy_v8liftoff, all_tests, interp_name="fizzy", compiler_name="v8-liftoff")
        plotCompilerSpeedup(df_wasm3_v8liftoff, all_tests, interp_name="wasm3", compiler_name="v8-liftoff")
        plotCompilerSpeedup(df_wasmi_wavm, all_tests, interp_name="wasmi", compiler_name="wavm")

        plotInterpOneEngine(df_interp, 'wasmi', all_tests, "Wasmi - all Precompiles (existing and proposed) compared")
        plotInterpOneEngine(df_interp, 'wabt', all_tests, "Wabt - all Precompiles (existing and proposed) compared")
        plotCompilerStackedOneTest(df_compiler, blake2b_test_names[2])
        plotCompilerStackedOneTest(df_compiler, "bls12-381-aggreg-128-pubkeys-verify-sig")
        plotCompilerStackedOneTest(df_native_and_compile, "bls12-381-aggreg-128-pubkeys-verify-sig", native=True)
    else:
        df_scout_rolluprs_bn128_pairings = df_scout_data[df_scout_data['bench_name'] == 'ecpairing-zkrollup-rust-wasm-bn128-two-pairings']

        df_rolluprs_native = df_scout_data[df_scout_data['bench_name'] == 'ecpairing-zkrollup-rust-native-bn128-two-pairings']
        df_rolluprs_native = df_rolluprs_native.fillna(0)

        df_scout_rolluprs = df_scout_rolluprs_bn128_pairings.append(df_rolluprs_native)

        df_scout_rolluprs = df_scout_rolluprs[df_scout_rolluprs['engine'].isin(
            ['rust-native', 'v8-liftoff', 'v8-turbofan', 'wabt-bignums-slowhost-slowmont', 'wabt-no-bignums']
        )]
            
        df_scout_rolluprs.replace('wabt-bignums-slowhost-slowmont', 'wabt-with-bignums', inplace=True)
        df_scout_means_rolluprs = df_scout_rolluprs.groupby(['engine']).mean()

        plotOneTestColoredTicks(df_scout_means_rolluprs,
            suptitle="rollup.rs-bn128-pairings - fast Scout engines (v8-liftoff and wabt-with-bignums)",
            suptitle_pos=1.02,
            subtitle="ecpairing-zkrollup-rust-wasm-bn128-two-pairings\n",
            subtitle_size='xx-large',
            highlight_tick="wabt-with-bignums")

        df_scout_websnark = df_scout_data[df_scout_data['bench_name'] == 'ecpairing-zkrollup-websnark-bn128-two-pairings']
        df_rolluprs_native = df_scout_data[df_scout_data['bench_name'] == 'ecpairing-zkrollup-rust-native-bn128-two-pairings']
        df_rolluprs_native = df_rolluprs_native.fillna(0)
        df_scout_websnark = df_scout_websnark.append(df_rolluprs_native)

        df_scout_websnark = df_scout_websnark[df_scout_websnark['engine'].isin(
            ['rust-native', 'v8-liftoff', 'v8-turbofan', 'wabt-bignums-slowhost-slowmont', 'wabt-bignums-slowhost-slowmont-superops']
        )]

        df_scout_websnark.replace('wabt-bignums-slowhost-slowmont', 'wabt-with-bignums', inplace=True)
        df_scout_websnark.replace('wabt-bignums-slowhost-slowmont-superops', 'wabt-bignums-superops', inplace=True)
        df_scout_means_websnark = df_scout_websnark.groupby(['engine']).mean()

        plotOneTestColoredTicks(df_scout_means_websnark,
            suptitle="websnark-bn128-pairings - engines compared (v8-liftoff and wabt-with-bignums)",
            suptitle_pos=1.02,
            subtitle="ecpairing-zkrollup-websnaark-bn128-two-pairings\n",
            subtitle_size='xx-large',
            highlight_tick="wabt-bignums-superops")
