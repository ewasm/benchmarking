Benchmarks are formatted as follows.

```
<engine> <contract> <instantiation time or invocation time> <list of comma separated times in mucroseconds>
```

The invocation time can be done only once, and corresponds to parsing/validating/compiling. The invocation time is for invocing an already instantiated contract.

The list of times are in order of the tests executed. To see the list of tests, see the `test_vectors` directory or the yml fillers.
