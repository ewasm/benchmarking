
SYSROOT=/home/user/repos/wasmception/sysroot
CC=/home/user/repos/wasmception/dist/bin/clang

.PHONY: all clean

all: sha256_1 sha256_2

sha256_1:
	$(CC) \
		--target=wasm32-unknown-unknown-wasm \
		--sysroot=$(SYSROOT) \
		-g \
		-Oz \
		-o sha256_1.wasm \
		-nostartfiles \
		-Wl,--allow-undefined-file=eei.syms,--demangle,--no-entry,--no-threads \
		-fvisibility=hidden \
		sha256_1.c

sha256_2:
	$(CC) \
		--target=wasm32-unknown-unknown-wasm \
		--sysroot=$(SYSROOT) \
		-g \
		-Oz \
		-o sha256_2.wasm \
		-nostartfiles \
		-Wl,--allow-undefined-file=eei.syms,--demangle,--no-entry,--no-threads \
		-fvisibility=hidden \
		sha256_2.c

clean:
	rm *.wasm
