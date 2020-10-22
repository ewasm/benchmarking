
pub fn bench() {
    let input: [u8; 68] = [ 38u8, 188u8, 235u8, 89u8, 128u8, 36u8, 49u8, 175u8, 203u8, 206u8, 31u8, 193u8, 148u8, 201u8, 234u8, 164u8, 23u8, 178u8, 251u8, 103u8, 220u8, 117u8, 169u8, 93u8, 176u8, 188u8, 126u8, 198u8, 177u8, 200u8, 175u8, 17u8, 223u8, 106u8, 29u8, 169u8, 161u8, 245u8, 170u8, 193u8, 55u8, 135u8, 100u8, 128u8, 37u8, 46u8, 93u8, 202u8, 198u8, 44u8, 53u8, 78u8, 192u8, 212u8, 43u8, 118u8, 176u8, 100u8, 43u8, 97u8, 129u8, 237u8, 9u8, 152u8, 73u8, 234u8, 29u8, 87u8 ];


    let mut x = bigint::uint::U256::from(&input[4..36]);
    let y = bigint::uint::U256::from(&input[36..68]);

    // based on https://github.com/gcolvin/evm-drag-race/blob/550e4e85f4db9c1485d01498d8033ef91c55cd78/mul256c.cpp

    for _i in 0..10000 {
        //x = x*y; x = x*y; x = x*y; x = x*y; x = x*y; x = x*y; x = x*y; x = x*y;
        //x = x*y; x = x*y; x = x*y; x = x*y; x = x*y; x = x*y; x = x*y; x = x*y;

        x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0;
        x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0;

        x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0;
        x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0;

        x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0;
        x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0;

        x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0;
        x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0;

        x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0;
        x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0;

        x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0;
        x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0;

        x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0;
        x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0;

        x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0;
        x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0; x = x.overflowing_mul(y).0;
    }

    let mut result = [0u8; 32];
    x.to_big_endian(&mut result);

    let expected: [u8; 32] = [ 128u8, 186u8, 248u8, 209u8, 131u8, 164u8, 22u8, 62u8, 54u8, 181u8, 7u8, 108u8, 138u8, 192u8, 137u8, 135u8, 29u8, 144u8, 243u8, 199u8, 94u8, 232u8, 143u8, 74u8, 2u8, 4u8, 202u8, 158u8, 194u8, 131u8, 61u8, 169u8 ];

    if result != expected {
        panic!("crash and burn");
    }

}