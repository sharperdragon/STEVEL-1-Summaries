import os

SUBDEX_PATH = './subdex'
OUTPUT_PATH = './static/nav.html'

entries = sorted(f for f in os.listdir(SUBDEX_PATH) if f.endswith('.html'))

with open(OUTPUT_PATH, 'w') as f:
    f.write('<nav style="margin: 10px 0; text-align: center;">\n')
    f.write('  <a href="index.html" class="nav-link"> HOME </a> | \n')
    for name in entries:
        label = name.replace('.html', '').capitalize()
        f.write(f'  <a href="subdex/{name}" class="nav-link">{label}</a> | \n')
    f.write('</nav>\n')

import json

MANIFEST_OUTPUT = './subdex/utils/table.manifest.json'
manifest_data = [{"name": name.replace('.html', '').capitalize(), "file": name} for name in entries]

with open(MANIFEST_OUTPUT, 'w') as mf:
    json.dump(manifest_data, mf, indent=2)