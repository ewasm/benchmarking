extern crate ethereum_bn128;
extern crate parity_bytes as bytes;

use bytes::BytesRef;

pub fn bench() {

    // gas logic is neglible, can exclude from benchmark
    /*
    // let length = ewasm_api::calldata_size();
    // charge a base fee plus a word fee for every element
    let base_fee = 100000;
    let element_fee = 80000;
    let total_cost = base_fee + (length / 192) * element_fee;
    ewasm_api::consume_gas(total_cost as u64);
    */

    // 00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002198e9393920d483a7260bfb731fb5d25f1aa493335a9e71297e485b7aef312c21800deef121f1e76426a00665e5c4479674322d4f75edadd46debd5cd992f6ed090689d0585ff075ec9e99ad690c3395bc4b313370b38ef355acdadcd122975b12c85ea5db8c6deb4aab71808dcb408fe3d1e7690c43d37b4ce6cc0166fa7daa00000000000000000000000000000000000000000000000000000000000000010000000000000000000000000000000000000000000000000000000000000002198e9393920d483a7260bfb731fb5d25f1aa493335a9e71297e485b7aef312c21800deef121f1e76426a00665e5c4479674322d4f75edadd46debd5cd992f6ed275dc4a288d1afb3cbb1ac09187524c7db36395df7be3b99e673b13a075a65ec1d9befcd05a5323e6da4d435f3b617cdb3af83285c2df711ef39c01571827f9d

    // let input: [u8; 384] = [ 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 1u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 2u8, 25u8, 142u8, 147u8, 147u8, 146u8, 13u8, 72u8, 58u8, 114u8, 96u8, 191u8, 183u8, 49u8, 251u8, 93u8, 37u8, 241u8, 170u8, 73u8, 51u8, 53u8, 169u8, 231u8, 18u8, 151u8, 228u8, 133u8, 183u8, 174u8, 243u8, 18u8, 194u8, 24u8, 0u8, 222u8, 239u8, 18u8, 31u8, 30u8, 118u8, 66u8, 106u8, 0u8, 102u8, 94u8, 92u8, 68u8, 121u8, 103u8, 67u8, 34u8, 212u8, 247u8, 94u8, 218u8, 221u8, 70u8, 222u8, 189u8, 92u8, 217u8, 146u8, 246u8, 237u8, 9u8, 6u8, 137u8, 208u8, 88u8, 95u8, 240u8, 117u8, 236u8, 158u8, 153u8, 173u8, 105u8, 12u8, 51u8, 149u8, 188u8, 75u8, 49u8, 51u8, 112u8, 179u8, 142u8, 243u8, 85u8, 172u8, 218u8, 220u8, 209u8, 34u8, 151u8, 91u8, 18u8, 200u8, 94u8, 165u8, 219u8, 140u8, 109u8, 235u8, 74u8, 171u8, 113u8, 128u8, 141u8, 203u8, 64u8, 143u8, 227u8, 209u8, 231u8, 105u8, 12u8, 67u8, 211u8, 123u8, 76u8, 230u8, 204u8, 1u8, 102u8, 250u8, 125u8, 170u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 1u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 2u8, 25u8, 142u8, 147u8, 147u8, 146u8, 13u8, 72u8, 58u8, 114u8, 96u8, 191u8, 183u8, 49u8, 251u8, 93u8, 37u8, 241u8, 170u8, 73u8, 51u8, 53u8, 169u8, 231u8, 18u8, 151u8, 228u8, 133u8, 183u8, 174u8, 243u8, 18u8, 194u8, 24u8, 0u8, 222u8, 239u8, 18u8, 31u8, 30u8, 118u8, 66u8, 106u8, 0u8, 102u8, 94u8, 92u8, 68u8, 121u8, 103u8, 67u8, 34u8, 212u8, 247u8, 94u8, 218u8, 221u8, 70u8, 222u8, 189u8, 92u8, 217u8, 146u8, 246u8, 237u8, 39u8, 93u8, 196u8, 162u8, 136u8, 209u8, 175u8, 179u8, 203u8, 177u8, 172u8, 9u8, 24u8, 117u8, 36u8, 199u8, 219u8, 54u8, 57u8, 93u8, 247u8, 190u8, 59u8, 153u8, 230u8, 115u8, 177u8, 58u8, 7u8, 90u8, 101u8, 236u8, 29u8, 155u8, 239u8, 205u8, 5u8, 165u8, 50u8, 62u8, 109u8, 164u8, 212u8, 53u8, 243u8, 182u8, 23u8, 205u8, 179u8, 175u8, 131u8, 40u8, 92u8, 45u8, 247u8, 17u8, 239u8, 57u8, 192u8, 21u8, 113u8, 130u8, 127u8, 157u8 ];

    {{input}}

    // NOTE: this validation will also be done by bn128_pairing
    if input.len() % 192 != 0 {
        panic!();
    }

    // let expected: [u8; 32] = [ 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 1u8 ];

    {{expected}}

    let mut output = [0u8; 32];
    match ethereum_bn128::bn128_pairing(&input[..], &mut BytesRef::Fixed(&mut output[..])) {
        Ok(_) => {
            // check that output is equal to expected
            if !(output).eq(expected.as_ref()) {
                panic!("crash and burn");
            }
        },
        Err(_) => panic!(),
    }

}