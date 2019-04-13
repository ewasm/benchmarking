#!/usr/bin/env python

"""

To run try eg:
python3 testcase_generator.py sha256 main.wat sha256.dat
where:
  sha256 means that it will output sha256Filler.yml.
  sha256.dat is test cases which are a newline delimited list with space delimited input and output.
    0x... 0x...
    0x... 0x...
  main.wat is the binaryen-produced wat file which takes input message from the dat file, and returns message to compare against the dat file.


current limitations:
 - For testing, the output must be 256 bits, since that is what fits in a storage location. This can be generalized when needed. But lets keep it simple for now.
 - It can handle at most 256 test cases. For more, we must reverse bytes of each storage key to be little-endian, since wasm will reverse them when they are written to memory.

"""

import os
import sys


def generate_test_filler(test_name, wat_filename, test_cases_filename):
  # get test cases
  f = open(test_cases_filename, 'r')
  test_cases = f.readlines()
  test_cases = [test_case[:-1].split(" ") for test_case in test_cases]

  # open yml file, print test name in first line
  f = open(test_name+"Filler.yml", 'w')
  f.write(test_name+":")

  # write the top of the yaml file
  f.write("""
  env:
    currentCoinbase: 2adc25665018aa1fe0e6bc666dac8fc2697ff9ba
    currentDifficulty: '0x020000'
    currentGasLimit: '89128960'
    currentNumber: '1'
    currentTimestamp: '1000'
    previousHash: 5e20a0453cecd065ea59c37ac63e079ee08998b6045136a8ce6635c7912ec0b6
  pre:
    a94f5374fce5edbc8e2a8697c15331677e6ebf0b:
      balance: '100000000000'
      code: ''
      nonce: '0'
      storage: {}
    1000000000000000000000000000000000000001:
      balance: '100000000000'
      code: |""")

  # print code section to call the precompile
  f.write("""
        (module
         (import "ethereum" "storageStore" (func $storageStore (param i32 i32)))
         (import "ethereum" "call"         (func $call (param i64 i32 i32 i32 i32) (result i32)))
         (import "ethereum" "returnDataCopy" (func $returnDataCopy (param i32 i32 i32)))
         ;;(import "debug" "printStorageHex" (func $printStorageHex (param i32)))
         ;;(import "debug" "printMemHex" (func $printMemHex (param i32 i32)))""")

  # compute number of Wasm memory pages needed
  total_memory_bytes = 0
  for test_case in test_cases:
    test_case = test_case[0][2:]
    total_memory_bytes += len(test_case)//2
  memory_pages_needed = total_memory_bytes//(2**16)+1
  f.write("""
         (memory """+str(memory_pages_needed)+""") """)
  # write address of contract containing the precompile
  f.write("""
         (data (i32.const 0) "\\b9\\4f\\53\\74\\fc\\e5\\ed\\bc\\8e\\2a\\86\\97\\c1\\53\\31\\67\\7e\\6e\\bf\\0b")
""")
  # init data segment with each test case input
  byte_location_of_test_case = 128
  for test_case in test_cases:
    test_case = test_case[0][2:]
    test_case_hex_special = ""
    for i in range(0,len(test_case),2):
      test_case_hex_special += "\\"+test_case[i:i+2]
    f.write("         (data (i32.const " + str(byte_location_of_test_case) + ") \"" + test_case_hex_special + "\")\n")
    byte_location_of_test_case += len(test_case)//2
  # continue writing wasm code
  f.write("""
         (export "main" (func $main))
         (export "memory" (memory 0))
         (func $main
          ;; memory looks like this
          ;; 0                     | 32          | 64            | 96                                  | 128...
          ;; address of precompile | wei to send | returned data | storage key to store returned value | data to process...""")
  # wasm code to execute each test case
  byte_location_of_test_case = 128
  for i,test_case in enumerate(test_cases):
    test_case_input = test_case[0][2:]
    test_case_output = test_case[1][2:]
    f.write("""


          ;; call the precompile at address b94...f0b and send value 0 Eth
          ;;                      gas           addrOffset     valOffset      dataOffset     dataLength
          (drop (call $call (i64.const 200000) (i32.const 0) (i32.const 32) (i32.const """+str(byte_location_of_test_case)+""") (i32.const """+ str(len(test_case_input)//2) +""")))
          ;; get return data
          ;;                     resultOffset   dataOffset    length
          (call $returnDataCopy (i32.const 64) (i32.const 0) (i32.const """+ str(len(test_case_output)//2) +"""))
          ;; store result in storage
          (i32.store8 (i32.const 127) (i32.const """+str(i)+"""))
          ;;                     pathOffset     valueOffset
          (call $storageStore (i32.const 96) (i32.const 64))
          ;;(call $printMemHex (i32.const 96) (i32.const 32))
          ;;(call $printStorageHex (i32.const 96))""")
    byte_location_of_test_case += len(test_case_input)//2
  # finish writing wasm code to call each test case
  f.write("""
         )
        )""")

  # print yml stuff after code
  f.write("""
      nonce: '0'
      storage: {}
    b94f5374fce5edbc8e2a8697c15331677e6ebf0b:
      balance: '100000000000'
      code: |
""")

  # print contract to be benchmakred
  f2 = open(wat_filename, 'r')
  wat_file = f2.readlines()
  wat_file = ["        "+line for line in wat_file]
  for line in wat_file:
    f.write(line)

  # print more yml stuff
  f.write("""
      nonce: ''
      storage: {}
  expect:
    - indexes:
        data: !!int -1
        gas: !!int -1
        value: !!int -1
      network:
        - ALL
      result:
        1000000000000000000000000000000000000001:
          storage: {
""")

  # print correct output to be checked against
  for i,test_case in enumerate(test_cases):
    f.write("            " + str(i) + ": '" + test_case[1] + "0"*(64-(len(test_case[1])-2)) + "'")
    if i!=len(test_cases)-1:
      f.write(",\n")
  # print final yml stuff
  f.write("""
            }
        b94f5374fce5edbc8e2a8697c15331677e6ebf0b:
          storage: {}
  transaction:
    data:
    - ''
    gasLimit:
    - '0x5000001'
    gasPrice: '0x01'
    nonce: '0x00'
    secretKey: 45a915e4d060149eb4365960e6a7a45f334393093061116b197e3240065ff2d8
    to: '1000000000000000000000000000000000000001'
    value:
    - '0'""")


if __name__ == "__main__":
  if len(sys.argv)!=4:
    print("Arguments should be: <testname eg sha256> <wat_filename>.wat <testcases_filename>.dat")
  else:
    generate_test_filler(sys.argv[1], sys.argv[2], sys.argv[3])


