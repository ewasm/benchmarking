var args = process.argv.slice(2);
var wasmfile = args[0];

console.log('args:', args);

console.log('---- reading wasm file..')
const readAsBinary = filename => {
if (typeof process === 'object' && typeof require === 'function') {
    const binary = require('fs').readFileSync(filename);
    return !binary.buffer ? new Uint8Array(binary) : binary;
} else
    return typeof readbuffer === 'function'
        ? new Uint8Array(readbuffer(filename))
        : read(filename, 'binary');
};

const wasmBytes = readAsBinary(wasmfile)

console.log('---- wasm file read.')

const imports = {
    env: {}
};

imports.env.memory = new WebAssembly.Memory({ initial: 10 })

console.time('instantiate');
WebAssembly.instantiate(wasmBytes, imports)
  .then(r => {
    console.timeEnd('instantiate');
    console.log('---- calling main...')
    console.time('run-main');
    try {
      const syncReturn = r.instance.exports.main();
      console.timeEnd('run-main');
      console.log('---- wasm returns:', syncReturn);
    } catch (e) {
      console.timeEnd('run-main');
      console.log('caught error:', e)
    }
  });
