/*
based on https://github.com/gcolvin/evm-drag-race/blob/550e4e85f4db9c1485d01498d8033ef91c55cd78/mul256.asm

remix input format: "0x802431afcbce1fc194c9eaa417b2fb67dc75a95db0bc7ec6b1c8af11df6a1da9", "0xa1f5aac137876480252e5dcac62c354ec0d42b76b0642b6181ed099849ea1d57"

calldata: 0x26bceb59802431afcbce1fc194c9eaa417b2fb67dc75a95db0bc7ec6b1c8af11df6a1da9a1f5aac137876480252e5dcac62c354ec0d42b76b0642b6181ed099849ea1d57

compiled with soljson-v0.5.1+commit.c8a2cb62.js
*/


pragma solidity ^0.5.1;

contract MUL256 {

    function mul256(uint256 x, uint256 y) public pure returns(bytes32 ret) {
        assembly {

            //let x := 0x802431afcbce1fc194c9eaa417b2fb67dc75a95db0bc7ec6b1c8af11df6a1da9
            //let y := 0xa1f5aac137876480252e5dcac62c354ec0d42b76b0642b6181ed099849ea1d57

            for { let i := 0 } lt(i, 10000) { i := add(i, 1) } {
                x := mul(y, mul(y, mul(y, mul(y, x))))
                x := mul(y, mul(y, mul(y, mul(y, x))))

                x := mul(y, mul(y, mul(y, mul(y, x))))
                x := mul(y, mul(y, mul(y, mul(y, x))))

                x := mul(y, mul(y, mul(y, mul(y, x))))
                x := mul(y, mul(y, mul(y, mul(y, x))))

                x := mul(y, mul(y, mul(y, mul(y, x))))
                x := mul(y, mul(y, mul(y, mul(y, x))))

                x := mul(y, mul(y, mul(y, mul(y, x))))
                x := mul(y, mul(y, mul(y, mul(y, x))))

                x := mul(y, mul(y, mul(y, mul(y, x))))
                x := mul(y, mul(y, mul(y, mul(y, x))))

                x := mul(y, mul(y, mul(y, mul(y, x))))
                x := mul(y, mul(y, mul(y, mul(y, x))))

                x := mul(y, mul(y, mul(y, mul(y, x))))
                x := mul(y, mul(y, mul(y, mul(y, x))))
            }

            ret := x
        }
    }
}
