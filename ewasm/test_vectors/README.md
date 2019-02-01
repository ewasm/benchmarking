Each test vector `.dat` file is a list of test vectors as follows

```
0x<input hex string> 0x<output hex string>
0x<input hex string> 0x<output hex string>
0x<input hex string> 0x<output hex string>
```

Current limitations:
 * The output must be 256 bits, since that is what fits in a storage location. This can be generalized to longer outputs when needed. But lets keep it simple for now. The input can be of arbitrary length.
 * It can handle at most 256 test cases. For more, we must reverse bytes of each storage key to be little-endian, since wasm will reverse them when they are written to memory.
 * There is no way to leave comments in the test vector files.

These limitations can be fixed in `ewasm_precompile_filler_generator.py` when needed.
