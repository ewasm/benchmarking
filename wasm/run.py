import re, glob
from subprocess import Popen, PIPE

def extract_output(output):
    reg = re.search('successfully in ([0-9]*)m+([0-9]*.*)s', output)
    compile_mins = reg.group(1)
    compile_secs = reg.group(2)
    reg = re.search('duration = (.*)', output)
    runtime = reg.group(1)

    print("compiled in {} minutes {} seconds".format(compile_mins, compile_secs))
    print("runtime {}".format(runtime))

    # return (compile_mins, compile_secs, runtime)

tests = glob.glob('build/target/wasm32-unknown-unknown/release/*.wasm')

for test in sorted(tests):
    print(test)
    pipe = Popen(['./life', '-polymerase', '-entry', 'ecadd_benchmark', test], stdout=PIPE)
    text = pipe.communicate()[0]
    print("return code is ", pipe.returncode)
    extract_output(text.decode('utf-8'))
