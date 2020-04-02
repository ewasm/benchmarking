extern crate num_bigint;

use num::{One, Zero};
use num_bigint::{BigInt, Sign};
use std::cmp;
use std::io::{self, Read};
use std::ops::{Rem, Shl};

const LENGTH_LENGTH: usize = 32;
const G_QUAD_DIVISOR: u64 = 20;

fn f(x: u64) -> u64 {
    match x {
        0...64 => x * x,
        65...1024 => (x * x / 4) + 96 * x - 3072,
        _ => (x * x / 16) + 480 * x - 199680,
    }
}

fn calculate_cost(lm: usize, lb: usize, exp: &BigInt) -> u64 {
    let le = exp.to_bytes_be().1.len();
    let lep: u64 = match le {
        0...32 => {
            if exp.is_zero() {
                0u64
            } else {
                exp.bits() as u64 - 1
            }
        }
        _ => {
            let nbits = exp.bits();
            let (loglow32bytes, low32bytes) = if nbits > 256 {
                let x = exp.rem(&BigInt::one().shl(256));
                (x.bits() - 1, x)
            } else {
                (nbits - 1, exp.clone())
            };

            if low32bytes > BigInt::zero() {
                8 * (le as u64 - 32) + loglow32bytes as u64
            } else {
                8 * (le as u64 - 32)
            }
        }
    };

    (f(cmp::max(lm, lb) as u64) * cmp::max(lep, 1 as u64)) / G_QUAD_DIVISOR
}

fn modexp(base: &BigInt, exp: &BigInt, modulus: &BigInt) -> Vec<u8> {
    let x = if modulus.is_zero() {
        BigInt::zero()
    } else {
        base.modpow(exp, modulus)
    };
    let (_, mut data) = x.to_bytes_be();

    /* padded on 32 bytes */
    let mut padded = vec![0u8; (32 - (data.len() % 32)) % 32];
    padded.append(&mut data);
    padded
}


pub fn bench() {
    use num::cast::ToPrimitive;

    // let input_size = ewasm_api::calldata_size();

    // let input: [u8; 225] = [ 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 64u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 1u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 0u8, 64u8, 224u8, 154u8, 217u8, 103u8, 84u8, 101u8, 197u8, 58u8, 16u8, 159u8, 172u8, 102u8, 164u8, 69u8, 201u8, 27u8, 41u8, 45u8, 43u8, 178u8, 197u8, 38u8, 138u8, 221u8, 179u8, 12u8, 216u8, 47u8, 128u8, 252u8, 176u8, 3u8, 63u8, 249u8, 124u8, 128u8, 165u8, 252u8, 111u8, 57u8, 25u8, 58u8, 233u8, 105u8, 198u8, 237u8, 230u8, 113u8, 10u8, 107u8, 122u8, 194u8, 112u8, 120u8, 160u8, 109u8, 144u8, 239u8, 28u8, 114u8, 229u8, 200u8, 95u8, 181u8, 2u8, 252u8, 158u8, 31u8, 107u8, 235u8, 129u8, 81u8, 101u8, 69u8, 151u8, 82u8, 24u8, 7u8, 94u8, 194u8, 175u8, 17u8, 140u8, 216u8, 121u8, 141u8, 246u8, 224u8, 138u8, 20u8, 124u8, 96u8, 253u8, 96u8, 149u8, 172u8, 43u8, 176u8, 44u8, 41u8, 8u8, 207u8, 77u8, 215u8, 200u8, 31u8, 17u8, 194u8, 137u8, 228u8, 188u8, 233u8, 143u8, 53u8, 83u8, 118u8, 143u8, 57u8, 42u8, 128u8, 206u8, 34u8, 191u8, 92u8, 79u8, 74u8, 36u8, 140u8, 107u8 ];

    {{input}}

    // let expected: [u8; 64] = [ 96u8, 0u8, 143u8, 22u8, 20u8, 204u8, 1u8, 220u8, 251u8, 107u8, 251u8, 9u8, 198u8, 37u8, 207u8, 144u8, 180u8, 125u8, 68u8, 104u8, 219u8, 129u8, 181u8, 248u8, 183u8, 163u8, 157u8, 66u8, 243u8, 50u8, 234u8, 185u8, 178u8, 218u8, 143u8, 45u8, 149u8, 49u8, 22u8, 72u8, 168u8, 242u8, 67u8, 244u8, 187u8, 19u8, 207u8, 179u8, 216u8, 247u8, 242u8, 163u8, 192u8, 20u8, 18u8, 46u8, 187u8, 62u8, 212u8, 27u8, 2u8, 120u8, 58u8, 220u8 ];

    {{expected}}

    let mut reader = input.chain(io::repeat(0));

    let mut length_bytes = [0u8; LENGTH_LENGTH];
    reader
        .read_exact(&mut length_bytes)
        .expect("Should be able to read 32 bytes from input");
    let base_length = BigInt::from_bytes_be(Sign::Plus, &length_bytes[..])
        .to_usize() // Get the `usize` version of base_length, as it won't
        .unwrap(); // be possible to read more anyway.

    reader
        .read_exact(&mut length_bytes)
        .expect("Should be able to read 32 bytes from input");
    let exp_length = BigInt::from_bytes_be(Sign::Plus, &length_bytes[..])
        .to_usize() // Same thing with exponent
        .unwrap();

    reader
        .read_exact(&mut length_bytes)
        .expect("Should be able to read 32 bytes from input");
    let mod_length = BigInt::from_bytes_be(Sign::Plus, &length_bytes[..])
        .to_usize()
        .unwrap();

    let mut base_bytes = vec![0u8; base_length];
    reader
        .read_exact(&mut base_bytes[..])
        .expect("Should be able to read base bytes from input");
    let base = BigInt::from_bytes_be(Sign::Plus, &base_bytes[..]);
    let mut exp_bytes = vec![0u8; exp_length];
    reader
        .read_exact(&mut exp_bytes[..])
        .expect("Should be able to read exp bytes from input");
    let exp = BigInt::from_bytes_be(Sign::Plus, &exp_bytes[..]);
    let mut mod_bytes = vec![0u8; mod_length];
    reader
        .read_exact(&mut mod_bytes[..])
        .expect("Should be able to read modulus bytes from input");
    let modulus = BigInt::from_bytes_be(Sign::Plus, &mod_bytes[..]);

    let _cost = calculate_cost(mod_length, base_length, &exp);

    // Geth's returns an empty array when base and mod both have
    // zero length.
    if base_length == 0 && mod_length == 0 {
        //ewasm_api::finish();
        return;
    }

    let output = modexp(&base, &exp, &modulus);
    //println!("output: {:?}", output);
    //println!("expected: {:?}", expected.as_ref());
    //ewasm_api::finish_data(&output[..])

    if output != expected.as_ref() {
        panic!("crash and burn");
    }

}
