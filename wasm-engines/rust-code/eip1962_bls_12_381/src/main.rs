mod bench;

use bench::bench;
use std::time::Instant;

fn main() {
    // fill input from template?

    let input = [0u8];
    let start = Instant::now();
    bench(&input);
    let duration = start.elapsed();

    println!("Time elapsed in bench() is: {:?}", duration);
}
