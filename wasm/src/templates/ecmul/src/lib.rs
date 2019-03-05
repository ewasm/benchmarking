extern crate ethereum_bn128;
extern crate parity_bytes as bytes;

use bytes::BytesRef;

#[cfg(not(test))]
#[no_mangle]
pub extern "C" fn main() {
    let input = {{ args }};
    let mut output = [0u8; 64];

    for i in input.iter() {
        match ethereum_bn128::bn128_mul(&i[..], &mut BytesRef::Fixed(&mut output[..])) {
            Ok(_) => { }
            Err(_) => { panic!("bn128 mul failed"); }
        }
    }
}
