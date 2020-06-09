all: notebook

# Default timeout is 30 seconds, but our cells are quite big, increase it to 120 seconds.
# More info: https://github.com/jupyter/nbconvert/issues/256#issuecomment-188405852
# TODO: upgrade to newer nbconvert which sets the timeout to off by default
notebook:
	cd notebooks && jupyter nbconvert --execute --ExecutePreprocessor.timeout=120 --to notebook --inplace wasm-engines.ipynb
