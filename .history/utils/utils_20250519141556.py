import os
import json

SUBDEX_PATH = './subdex'
NAV_OUTPUT_DIR = './utils/navs'
MANIFEST_OUTPUT = './static/table.manifest.json'
TABLE_SUFFIX = '.table.html'

def clean_label(filename):
    name = filename.replace(TABLE_SUFFIX, '')
    return name.replace('_', ' ').replace('-', ' ').title()

def strip_table_suffix(filename):
    return filename.replace(TABLE_SUFFIX, '')

entries = sorted(
    f for f in os.listdir(SUBDEX_PATH)
    if f.endswith(TABLE_SUFFIX)
)

os.makedirs(NAV_OUTPUT_DIR, exist_ok=True)

for entry in entries:
    name = strip_table_suffix(entry)
    nav_path = os.path.join(NAV_OUTPUT_DIR, f'nav_{name}.html')
    with open(nav_path, 'w') as f:
        f.write('<nav style="margin: 10px 0; text-align: center;">\n')
        f.write('  <a href="../index.html" class="nav-link"> HOME </a> |\n')
        for other in entries:
            if other == entry:
                continue
            other_name = strip_table_suffix(other)
            label = clean_label(other)
            f.write(f'  <a href="{other_name}.html" class="nav-link">{label}</a> |\n')
        f.write('</nav>\n')

manifest_data = [{"name": clean_label(e), "file": f"{strip_table_suffix(e)}.html"} for e in entries]

with open(MANIFEST_OUTPUT, 'w') as mf:
    json.dump(manifest_data, mf, indent=2)