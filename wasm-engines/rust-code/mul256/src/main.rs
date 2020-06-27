mod bench;

use std::time::{Instant};

pub fn main() {
    let start = Instant::now();
    bench::bench();
    let duration = start.elapsed();

    println!("Time elapsed in bench() is: {:?}", duration);
}
