extern crate tiny_keccak;

#[no_mangle]
pub extern "C" fn keccak_memptr(ptr: *const u8, size: usize) {
    let input = unsafe { ::std::slice::from_raw_parts(ptr, size) };

    let mut output = [0u8; 32];
    tiny_keccak::Keccak::keccak256(&input, &mut output);
}

#[no_mangle]
pub extern "C" fn keccak_memptr_loop(ptr: *const u8, size: usize, loop_count: usize) {
    let input = unsafe { ::std::slice::from_raw_parts(ptr, size) };

    let mut output = [0u8; 32];
    for i in 0..loop_count {
        tiny_keccak::Keccak::keccak256(&input, &mut output);
    }
}

#[no_mangle]
pub extern "C" fn keccak_predefined_data(loop_count: usize) {
    let mut input = [0u8; 256];

    let mut output = [0u8; 32];
    for i in 0..loop_count {
        input[0] = i as u8;
        tiny_keccak::Keccak::keccak256(&input, &mut output);
    }
}
