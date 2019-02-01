Each file is a list of test vectors as follows

```
0x<input hex string> 0x<output hex string>
0x<input hex string> 0x<output hex string>
0x<input hex string> 0x<output hex string>
...

One current limitation is that the output is at most 256-bits, this can be fixed in `ewasm_precompile_filler_generator.py` when it is needed. The input hex string is of arbitrary length.
```
