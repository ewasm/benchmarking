extern crate wee_alloc;

#[global_allocator]
static ALLOC: wee_alloc::WeeAlloc = wee_alloc::WeeAlloc::INIT;

mod bench;

#[no_mangle]
pub extern "C" fn main() {
    bench::bench();
}