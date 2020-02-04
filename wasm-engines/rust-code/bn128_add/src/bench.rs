extern crate ethereum_bn128;
extern crate parity_bytes as bytes;

use bytes::BytesRef;

pub fn bench() {

    // let input: [u8; 128] = [ 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 1u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 2u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 1u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 2u8 ];

    {{input}}

    // let expected: [u8; 64] = [ 3u8, 6u8, 68u8, 231u8, 46u8, 19u8, 26u8, 2u8, 155u8, 133u8, 4u8, 91u8, 104u8, 24u8, 21u8, 133u8, 217u8, 120u8, 22u8, 169u8, 22u8, 135u8, 28u8, 168u8, 211u8, 194u8, 8u8, 193u8, 109u8, 135u8, 207u8, 211u8, 21u8, 237u8, 115u8, 140u8, 14u8, 10u8, 124u8, 146u8, 231u8, 132u8, 95u8, 150u8, 178u8, 174u8, 156u8, 10u8, 104u8, 166u8, 164u8, 73u8, 227u8, 83u8, 143u8, 199u8, 255u8, 62u8, 191u8, 122u8, 90u8, 24u8, 162u8, 196u8 ];

    {{expected}}

    let mut output = [0u8; 64];
    match ethereum_bn128::bn128_add(&input[..], &mut BytesRef::Fixed(&mut output[..])) {
        Ok(_) => {
            if !(output).eq(expected.as_ref()) {
                panic!("crash and burn");
            }
        },
        Err(_) => panic!(),
    }

}