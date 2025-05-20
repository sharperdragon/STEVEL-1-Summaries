from pathlib import Path
from pathlib import Path
from bs4 import BeautifulSoup

BASE_HTML_PATH = Path("subdex/Base.html")
TABLE_DIR = Path("subdex/")
NAV_DIR = Path("utils/navs/")
OUTPUT_DIR = Path("pages/")

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