import json
import base64
import re

def extract_image(cell):
    for output in cell['outputs']:
        if 'data' in output and 'image/png' in output['data']:
            return base64.decodebytes(output['data']['image/png'].encode('utf-8'))

notebook_json = None
with open('wasm-engines.ipynb') as f:
    notebook_json = json.load(f)

for i, cell in enumerate(notebook_json['cells']):
    if cell['cell_type'] == 'code':
        file_name = re.search("# *save_image\('(.*)'\)", "".join(cell['source']))

        if file_name and file_name.group(1):
            file_name = file_name.group(1)
        else:
            continue

        # find the image binary in the metadata
        image = extract_image(cell)

        # save the image
        with open(file_name, 'wb') as f:
            f.write(image)
