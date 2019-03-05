extern crate ed25519_dalek;
extern crate sha2;

mod verify;

static input: [[u8; 128]; 100]  = [
{{ args }}
];

#[cfg(not(test))]
#[no_mangle]
pub extern "C" fn main() {
    for i in input.iter() {
			match verify::verify(&i) {
				Ok(true) => {
					continue;
				},
				Ok(false) => {
					panic!("failed");
				}
				Err(_) => {
					panic!("failed");
				}
			}
	}
}
