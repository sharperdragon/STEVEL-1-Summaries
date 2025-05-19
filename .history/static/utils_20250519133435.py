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