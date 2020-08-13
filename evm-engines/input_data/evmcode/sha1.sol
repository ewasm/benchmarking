// derived from https://github.com/ensdomains/solsha1/blob/master/contracts/SHA1.sol
// deployed ENS code at: https://etherscan.io/address/0x4e89a683dade995736457bde623e75f5840c2d34#code

// compiled with solc version:0.5.4+commit.9549d8ff.Emscripten.clang with optimizer enabled


/*
var definition = `[{"constant":true,"inputs":[{"name":"data","type":"bytes"}],"name":"sha1","outputs":[{"name":"ret","type":"bytes20"}],"payable":false,"stateMutability":"pure","type":"function"}]`;
*/

/*

	// sha1 test vectors from https://csrc.nist.gov/projects/cryptographic-algorithm-validation-program/secure-hashing#shavs
	// FIPS 180-4 "SHA Test Vectors for Hashing Byte-Oriented Messages"

	input := common.Hex2Bytes("{{input}}")
	// contract returns padded bytes "a94d7bf363f32a5a5b6e9f71b2edaa3f2ae31a61000000000000000000000000"
	expected := "{{expected}}000000000000000000000000"

	calldata, err := abi.Pack("sha1", input)

*/


pragma solidity ^0.5.1;

contract SHA1 {

    function sha1(bytes memory data) public pure returns(bytes20 ret) {
        assembly {
            // Get a safe scratch location
            let scratch := mload(0x40)

            // Get the data length, and point data at the first byte
            let len := mload(data)
            data := add(data, 32)

            // Find the length after padding
            let totallen := add(and(add(len, 1), 0xFFFFFFFFFFFFFFC0), 64)
            switch lt(sub(totallen, len), 9)
            case 1 { totallen := add(totallen, 64) }

            let h := 0x6745230100EFCDAB890098BADCFE001032547600C3D2E1F0

            function readword(ptr, off, count) -> result {
                result := 0
                if lt(off, count) {
                    result := mload(add(ptr, off))
                    count := sub(count, off)
                    if lt(count, 32) {
                        let mask := not(sub(exp(256, sub(32, count)), 1))
                        result := and(result, mask)
                    }
                }
            }

            for { let i := 0 } lt(i, totallen) { i := add(i, 64) } {
                mstore(scratch, readword(data, i, len))
                mstore(add(scratch, 32), readword(data, add(i, 32), len))

                // If we loaded the last byte, store the terminator byte
                switch lt(sub(len, i), 64)
                case 1 { mstore8(add(scratch, sub(len, i)), 0x80) }

                // If this is the last block, store the length
                switch eq(i, sub(totallen, 64))
                case 1 { mstore(add(scratch, 32), or(mload(add(scratch, 32)), shl(3, len))) }

                // Expand the 16 32-bit words into 80
                for { let j := 64 } lt(j, 128) { j := add(j, 12) } {
                    let temp := xor(xor(mload(add(scratch, sub(j, 12))), mload(add(scratch, sub(j, 32)))), xor(mload(add(scratch, sub(j, 56))), mload(add(scratch, sub(j, 64)))))
                    temp := or(and(shl(1, temp), 0xFFFFFFFEFFFFFFFEFFFFFFFEFFFFFFFEFFFFFFFEFFFFFFFEFFFFFFFEFFFFFFFE), and(shr(31, temp), 0x0000000100000001000000010000000100000001000000010000000100000001))
                    mstore(add(scratch, j), temp)
                }
                for { let j := 128 } lt(j, 320) { j := add(j, 24) } {
                    let temp := xor(xor(mload(add(scratch, sub(j, 24))), mload(add(scratch, sub(j, 64)))), xor(mload(add(scratch, sub(j, 112))), mload(add(scratch, sub(j, 128)))))
                    temp := or(and(shl(2, temp), 0xFFFFFFFCFFFFFFFCFFFFFFFCFFFFFFFCFFFFFFFCFFFFFFFCFFFFFFFCFFFFFFFC), and(shr(30, temp), 0x0000000300000003000000030000000300000003000000030000000300000003))
                    mstore(add(scratch, j), temp)
                }

                let x := h
                let f := 0
                let k := 0
                for { let j := 0 } lt(j, 80) { j := add(j, 1) } {
                    switch div(j, 20)
                    case 0 {
                        // f = d xor (b and (c xor d))
                        f := xor(shr(80, x), shr(40, x))
                        f := and(shr(120, x), f)
                        f := xor(shr(40, x), f)
                        k := 0x5A827999
                    }
                    case 1{
                        // f = b xor c xor d
                        f := xor(shr(120, x), shr(80, x))
                        f := xor(shr(40, x), f)
                        k := 0x6ED9EBA1
                    }
                    case 2 {
                        // f = (b and c) or (d and (b or c))
                        f := or(shr(120, x), shr(80, x))
                        f := and(shr(40, x), f)
                        f := or(and(shr(120, x), shr(80, x)), f)
                        k := 0x8F1BBCDC
                    }
                    case 3 {
                        // f = b xor c xor d
                        f := xor(shr(120, x), shr(80, x))
                        f := xor(shr(40, x), f)
                        k := 0xCA62C1D6
                    }
                    // temp = (a leftrotate 5) + f + e + k + w[i]
                    let temp := and(shr(187, x), 0x1F)
                    temp := or(and(shr(155, x), 0xFFFFFFE0), temp)
                    temp := add(f, temp)
                    temp := add(and(x, 0xFFFFFFFF), temp)
                    temp := add(k, temp)
                    temp := add(shr(224, mload(add(scratch, shl(2, j)))), temp)
                    //x := or(div(x, 0x10000000000), mul(temp, 0x10000000000000000000000000000000000000000))
                    x := or(shr(40, x), shl(160, temp))
                    x := or(and(x, 0xFFFFFFFF00FFFFFFFF000000000000FFFFFFFF00FFFFFFFF), shl(80, or(and(shr(50, x), 0xC0000000), and(shr(82, x), 0x3FFFFFFF))))
                }

                h := and(add(h, x), 0xFFFFFFFF00FFFFFFFF00FFFFFFFF00FFFFFFFF00FFFFFFFF)
            }
            ret := shl(96, or(or(or(or(and(shr(32, h), 0xFFFFFFFF00000000000000000000000000000000), and(shr(24, h), 0xFFFFFFFF000000000000000000000000)), and(shr(16, h), 0xFFFFFFFF0000000000000000)), and(shr(8, h), 0xFFFFFFFF00000000)), and(h, 0xFFFFFFFF)))
        }
        
    }
}

