extern crate ethereum_bn128;
extern crate parity_bytes as bytes;

use bytes::BytesRef;

pub fn bench() {

    // let input: [u8; 96] = [ 3u8, 151u8, 48u8, 234u8, 141u8, 255u8, 18u8, 84u8, 192u8, 254u8, 233u8, 192u8, 234u8, 119u8, 125u8, 41u8, 169u8, 199u8, 16u8, 183u8, 230u8, 22u8, 104u8, 63u8, 25u8, 79u8, 24u8, 196u8, 59u8, 67u8, 184u8, 105u8, 7u8, 58u8, 95u8, 252u8, 198u8, 252u8, 122u8, 40u8, 195u8, 7u8, 35u8, 214u8, 229u8, 140u8, 229u8, 119u8, 53u8, 105u8, 130u8, 214u8, 91u8, 131u8, 58u8, 90u8, 92u8, 21u8, 191u8, 144u8, 36u8, 180u8, 61u8, 152u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8, 255u8 ];

    {{input}}

    // let expected: [u8; 64] = [ 0u8, 161u8, 162u8, 52u8, 208u8, 142u8, 250u8, 162u8, 97u8, 102u8, 7u8, 227u8, 30u8, 202u8, 25u8, 128u8, 18u8, 139u8, 0u8, 180u8, 21u8, 200u8, 69u8, 255u8, 37u8, 187u8, 163u8, 175u8, 203u8, 129u8, 220u8, 0u8, 36u8, 32u8, 119u8, 41u8, 14u8, 211u8, 57u8, 6u8, 174u8, 184u8, 228u8, 47u8, 217u8, 140u8, 65u8, 188u8, 185u8, 5u8, 123u8, 160u8, 52u8, 33u8, 175u8, 63u8, 45u8, 8u8, 207u8, 196u8, 65u8, 24u8, 96u8, 36u8 ];

    {{expected}}

    let mut output = [0u8; 64];
    match ethereum_bn128::bn128_mul(&input[..], &mut BytesRef::Fixed(&mut output[..])) {
        Ok(_) => {
            if !(output).eq(expected.as_ref()) {
                panic!("crash and burn");
            }
        },
        Err(_) => panic!(),
    }

}