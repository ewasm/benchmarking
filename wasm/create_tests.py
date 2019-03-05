import jinja2, json, shutil, os, errno
from functools import reduce

# get a string containing a rust array of bytes
def get_rust_bytes(hex_str):
    tmp = map(''.join, zip(*[iter(hex_str)]*2))
    tmp = map(lambda x: int(x, 16), tmp)
    tmp = map(lambda x: '{}'.format(x)+'u8', tmp)
    tmp = reduce(lambda x, y: x+', '+y, tmp)
    return '[ '+tmp+' ],'

# use jinja templating engine to create a filled test file
def fill_template(template_file, args):
    templateLoader = jinja2.FileSystemLoader(os.path.dirname(template_file))
    templateEnv = jinja2.Environment(loader=templateLoader)
    template = templateEnv.get_template(os.path.split(template_file)[1])
    outputText = template.render(args)  # this is where to put args to the template renderer
    return outputText

def add_test_case(precompile, test):
    pass

def create_project_manifest():
    pass

# 'fills' template files and creates a new rust project
def create_project(precompile, test):
    test_name = test['name']
    test_input = test['input']

    try:
        shutil.rmtree('build/'+precompile+'/'+test_name)
    except OSError as exc:
        if exc.errno != errno.ENOENT:
            raise
        pass

    test_dir = 'build/'+precompile+'/'+test_name

    os.makedirs('build/'+precompile, exist_ok=True)
    shutil.copytree('src/templates/'+precompile, test_dir)

    filled = fill_template(test_dir+'/src/lib.rs', { 'args': test_input })
    with open(test_dir+'/src/lib.rs', 'w') as f:
        f.write(filled)

    filled = fill_template(test_dir+'/Cargo.toml', { 'args': precompile + '-' + test_name })
    with open(test_dir+'/Cargo.toml', 'w') as f:
        f.write(filled)

def create_cargo_workspace(items):
    shutil.copyfile('src/templates/Cargo.toml', 'build/Cargo.toml')
    filled_cargo = fill_template('build/Cargo.toml', { 'args': items })
    with open('build/Cargo.toml', 'w') as f:
        f.write(filled_cargo)

def main():
    ecadd_tests = None
    ecmul_tests = None
    inputs = {}

    with open('src/tests/ecadd.json') as f:
        ecadd_tests = json.load(f)
    

    with open('src/tests/ecmul.json') as f:
        ecmul_tests = json.load(f)

    for test in ecadd_tests['entries']:
        case = get_rust_bytes(test['input'])
        test_input = [ case for c in range(0,128) ]
        test_input = '[ ' + ''.join(test_input)[:-1] + ' ]'
        create_project('ecadd', {'name': test['name'], 'input': test_input})


    for test in ecmul_tests['entries']:
        case = get_rust_bytes(test['input'])
        test_input = [ case for c in range(0,128) ]
        test_input = '[ ' + ''.join(test_input)[:-1] + ' ]'
        create_project('ecmul', {'name': test['name'], 'input': test_input})

    ecadd_members = str(list(map(lambda x: 'ecadd/'+x['name'], ecadd_tests['entries']))).strip('[').strip(']')
    ecmul_members = str(list(map(lambda x: 'ecmul/'+x['name'], ecmul_tests['entries']))).strip('[').strip(']')
    create_cargo_workspace(ecadd_members + ', ' + ecmul_members)

if __name__ == "__main__":
    main()
