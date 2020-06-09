all: notebook

notebook:
	cd notebooks && jupyter nbconvert --execute --to notebook --inplace wasm-engines.ipynb
