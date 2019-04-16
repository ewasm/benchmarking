
/*

Implemented following: Knuth TAOCP, Volume 3, section 4.3.1, algorithm M: Multiplication of nonnegative integers. But since modulo 2^256, removed as many multiplcations as possible.



Compiles with the following (need a specific version of wasmception, and need pywebassembly for post-processing)

WASMCEPTION_DIR=/home/user/repos/benchmarking2/wasmception2
$WASMCEPTION_DIR/dist/bin/clang --target=wasm32-unknown-unknown-wasm --sysroot=$WASMCEPTION_DIR/sysroot -O3 -g -o mul256_C.wasm -nostartfiles -Wl,--allow-undefined-file=c_undefined.syms,--demangle,--no-entry,--no-threads -Wl,--export=_main -fvisibility=hidden mul256.c
PYTHONPATH="${PYTHONPATH}:/home/user/repos/benchmarking2/pywebassembly/"
export PYTHONPATH
python3 /home/user/repos/benchmarking2/pywebassembly/examples/ewasmify.py mul256_C.wasm

*/


// to avoid includes from libc, just hard-code things
typedef unsigned char uint8_t;
typedef unsigned int uint32_t;
typedef unsigned long long uint64_t;


// types used for Ethereum stuff
typedef uint8_t* bytes; // an array of bytes with unrestricted length
typedef uint8_t bytes32[32]; // an array of 32 bytes
typedef uint8_t address[20]; // an array of 20 bytes
typedef unsigned __int128 u128; // a 128 bit number, represented as a 16 bytes long little endian unsigned integer in memory
//typedef uint256_t u256; // a 256 bit number, represented as a 32 bytes long little endian unsigned integer in memory
typedef uint32_t i32; // same as i32 in WebAssembly
typedef uint32_t i32ptr; // same as i32 in WebAssembly, but treated as a pointer to a WebAssembly memory offset
typedef uint64_t i64; // same as i64 in WebAssembly

// functions for ethereum stuff
void useGas(i64 amount);
void getCaller(i32ptr* resultOffset);
   // memory offset to load the address into (address)
i32 getCallDataSize();
void callDataCopy(i32ptr* resultOffset, i32 dataOffset, i32 length);
   // memory offset to load data into (bytes), the offset in the input data, the length of data to copy
void revert(i32ptr* dataOffset, i32 dataLength);
void finish(i32ptr* dataOffset, i32 dataLength);
void storageStore(i32ptr* pathOffset, i32ptr* resultOffset);
void storageLoad(i32ptr* pathOffset, i32ptr* resultOffset);
   //the memory offset to load the path from (bytes32), the memory offset to store/load the result at (bytes32)
void printMemHex(i32ptr* offset, i32 length);
void printStorageHex(i32ptr* key);




// output is global so that it is allocated to memory, otherwise must pass as arg
uint32_t out[] = {0,0,0,0,0,0,0,0};




#define ITER(a,b,c) \
  t = (uint64_t)(u[a]) * (uint64_t)(v[b]) + w[c] + k; \
  w[c] = (uint32_t)t; \
  k = t >> 32;  //carry

#define ITERLAST(a,b,c) \
  t = (uint64_t)(u[a]) * (uint64_t)(v[b]) + w[c] + k; \
  w[c] = (uint32_t)t; \
  k = 0;


// takes two 256-bit values, each as 8 32-bit limbs, and multiplies them modulo 2^256
// algorithm and notation taken from Knuth TAOCP, Volume 3, section 4.3.1, algorithm M, but some multiplications can be omitted, and everything is unrolled for speed
uint32_t* mul256(uint32_t *u_in, uint32_t* v_in){

  uint32_t u[] = {u_in[0],u_in[1],u_in[2],u_in[3],u_in[4],u_in[5],u_in[6],u_in[7]};
  uint32_t v[] = {v_in[0],v_in[1],v_in[2],v_in[3],v_in[4],v_in[5],v_in[6],v_in[7]};
  uint32_t w[] = {0,0,0,0,0,0,0,0};

  uint32_t k = 0; //carry
  uint64_t t = 0;

  ITER(7,7,7)
  ITER(6,7,6)
  ITER(5,7,5)
  ITER(4,7,4)
  ITER(3,7,3)
  ITER(2,7,2)
  ITER(1,7,1)
  ITERLAST(0,7,0)
  ITER(7,6,6)
  ITER(6,6,5)
  ITER(5,6,4)
  ITER(4,6,3)
  ITER(3,6,2)
  ITER(2,6,1)
  ITERLAST(1,6,0)
  ITER(7,5,5)
  ITER(6,5,4)
  ITER(5,5,3)
  ITER(4,5,2)
  ITER(3,5,1)
  ITERLAST(2,5,0)
  ITER(7,4,4)
  ITER(6,4,3)
  ITER(5,4,2)
  ITER(4,4,1)
  ITERLAST(3,4,0)
  ITER(7,3,3)
  ITER(6,3,2)
  ITER(5,3,1)
  ITERLAST(4,3,0)
  ITER(7,2,2)
  ITER(6,2,1)
  ITERLAST(5,2,0)
  ITER(7,1,1)
  ITERLAST(6,1,0)
  ITERLAST(7,0,0)

  for (int i=0; i<8; ++i)
    out[i]=w[i];

  return out;

}




void bench(uint32_t* x, uint32_t* y){
  for( int i=0; i<10000; ++i ){
    x = mul256(y,mul256(y,mul256(y,mul256(y,x))));
    x = mul256(y,mul256(y,mul256(y,mul256(y,x))));
    x = mul256(y,mul256(y,mul256(y,mul256(y,x))));
    x = mul256(y,mul256(y,mul256(y,mul256(y,x))));

    x = mul256(y,mul256(y,mul256(y,mul256(y,x))));
    x = mul256(y,mul256(y,mul256(y,mul256(y,x))));
    x = mul256(y,mul256(y,mul256(y,mul256(y,x))));
    x = mul256(y,mul256(y,mul256(y,mul256(y,x))));

    x = mul256(y,mul256(y,mul256(y,mul256(y,x))));
    x = mul256(y,mul256(y,mul256(y,mul256(y,x))));
    x = mul256(y,mul256(y,mul256(y,mul256(y,x))));
    x = mul256(y,mul256(y,mul256(y,mul256(y,x))));

    x = mul256(y,mul256(y,mul256(y,mul256(y,x))));
    x = mul256(y,mul256(y,mul256(y,mul256(y,x))));
    x = mul256(y,mul256(y,mul256(y,mul256(y,x))));
    x = mul256(y,mul256(y,mul256(y,mul256(y,x))));
  }
}





bytes32 value_x[1] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
bytes32 value_y[1] = {0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};

// ewasm entry point
void _main(){

  callDataCopy((i32ptr*)value_x, 4, 32);
  callDataCopy((i32ptr*)value_y, 36, 32);

  bench((uint32_t*)value_x,(uint32_t*)value_y);

  finish((i32ptr*)value_x, 32);

}





// this test passes. These values were cross-tested in python.
int test(){

  // test values found https://github.com/cdetrio/fluence-wasm-bencher/blob/evm-runner/evmrace/ewasm-code/mul256/src/lib.rs
  uint32_t x[] = {2149855663, 3419283393, 2496260772, 397605735, 3698698589, 2965143238, 2982719249, 3748273577};
  uint32_t y[] = {2717231809, 931619968, 623795658, 3324785998, 3235130230, 2959354721, 2179795352, 1240079703};
  uint32_t* out = mul256(x,y);
  uint32_t out_correct[] = {3394174510, 1855079414, 1621212820, 1846600096, 2986217620, 3881882806, 1184205870, 1072052591};
  for (int i=0; i<8; i++){
    if(out[i]!=out_correct[i])
      return -1;
  }

  return 0;
}




// can export start fuction
/*
void _start(){
  _main();
}
*/
