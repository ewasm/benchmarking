
pub fn bench() {
    {{input}}


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

    {{expected}}

    if result != expected {
        panic!("crash and burn");
    }

}
