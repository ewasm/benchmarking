mod bench;

use bench::bench;

fn main() {
    let start = Instant::now();
    bench();
    let duration = start.elapsed();

    println!("Time elapsed in bench() is: {:?}", duration);
}
