import os
import json

SUBDEX_PATH = './subdex'
NAV_OUTPUT_DIR = './utils'
MANIFEST_OUTPUT = './static/table.manifest.json'

def clean_label(filename):
    name = filename.replace('.html', '')
    return name.replace('_', ' ').replace('-', ' ').title()

entries = sorted(
    f for f in os.listdir(SUBDEX_PATH)
    if f.endswith('.html') and not f.startswith('template')
)

# Write individual nav files excluding self-link
for name in entries:
    nav_path = os.path.join(NAV_OUTPUT_DIR, f'nav_{name}')
    with open(nav_path, 'w') as f:
        f.write('<nav style="margin: 10px 0; text-align: center;">\n')
        f.write('  <a href="../index.html" class="nav-link"> HOME </a> |\n')
        for other in entries:
            if other == name:
                continue
            label = clean_label(other)
            f.write(f'  <a href="{other}" class="nav-link">{label}</a> |\n')
        f.write('</nav>\n')

# Write manifest file
manifest_data = [{"name": clean_label(name), "file": name} for name in entries]
with open(MANIFEST_OUTPUT, 'w') as mf:
    json.dump(manifest_data, mf, indent=2)