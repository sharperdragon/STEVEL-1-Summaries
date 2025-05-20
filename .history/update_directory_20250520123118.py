import os
import json
from pathlib import Path
from bs4 import BeautifulSoup


BASE_HTML_PATH = Path("subdex/Base.html")
TABLE_DIR = Path("subdex/")
NAV_DIR = Path("utils/navs/")
OUTPUT_DIR = Path("pages/")
SUBDEX_PATH = './subdex'
NAV_OUTPUT_DIR = './utils/navs'
MANIFEST_OUTPUT = './static/table.manifest.json'
TABLE_SUFFIX = '.table.html'


def add_quiz_answer_classes(table_dir="subdex/"):
    table_dir = Path(table_dir)
    files = list(table_dir.glob("*.table.html"))

    for path in files:
        soup = BeautifulSoup(path.read_text(), "html.parser")
        modified = False

        for td in soup.find_all("td"):
            if "quiz-answer" not in td.get("class", []) and td.find("ul"):
                td["class"] = td.get("class", []) + ["quiz-answer"]
                modified = True

        if modified:
            path.write_text(str(soup))
            print(f"✅ Updated: {path.name}")
        else:
            print(f"➖ No change: {path.name}")



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
    nav_path = os.path.join(NAV_OUTPUT_DIR, f'nav_{name}table.html')
    with open(nav_path, 'w') as f:
        f.write('<nav style="margin: 10px 0; text-align: center;">\n')
        f.write('  <a href="../index.html" class="nav-link"> HOME </a> |\n')
        for other in entries:
            if other == entry:
                continue
            other_name = strip_table_suffix(other)
            label = clean_label(other)
            f.write(f'  <a href="{other_name}.table.html" class="nav-link">{label}</a> |\n')
        f.write('</nav>\n')

manifest_data = [
    {"name": clean_label(e), "file": f"{strip_table_suffix(e)}.table.html"}
    for e in entries
]

with open(MANIFEST_OUTPUT, 'w') as mf:
    json.dump(manifest_data, mf, indent=2)





def 
add_quiz_answer_classes()  # ✅ Ensure quiz-answer class is applied before HTML output

def clean_title(name):
    return name.replace('.table.html', '').replace('_', ' ').title()

base_template = BASE_HTML_PATH.read_text()

for table_file in TABLE_DIR.glob("*.table.html"):
    name = table_file.stem.replace(".table", "")  # 'autoantibodies' from 'autoantibodies.table.html'
    nav_file = NAV_DIR / f"nav_{name}.html"
    output_file = OUTPUT_DIR / f"{name}.html"

    table_html = table_file.read_text()
    nav_html = nav_file.read_text() if nav_file.exists() else "<!-- No nav -->"
    page_title = clean_title(table_file.name)

    output_html = base_template
    output_html = output_html.replace("{{PAGE_TITLE}}", page_title)
    output_html = output_html.replace("{{NAV_CONTENT}}", nav_html)
    output_html = output_html.replace("{{TABLE_CONTENT}}", table_html)

    output_file.write_text(output_html)
    print(f"✅ Built {output_file}")