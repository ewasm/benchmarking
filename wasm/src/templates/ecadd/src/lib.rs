extern crate ethereum_bn128;
extern crate ewasm_api;
extern crate parity_bytes as bytes;

use bytes::BytesRef;

#[cfg(not(test))]
#[no_mangle]
pub extern "C" fn ecadd_benchmark() {
    let mut output = [0u8; 64];
    let inputs = {{ args }};

    for input in inputs.iter() {
        match ethereum_bn128::bn128_add(&input[..], &mut BytesRef::Fixed(&mut output[..])) {
            Err(_) => { panic!("bn128 add failed"); }
            Ok(_) => { }
        }
    }
}
