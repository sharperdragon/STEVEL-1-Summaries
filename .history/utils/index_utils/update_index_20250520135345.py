

from pathlib import Path
import json

BASE_PATH = Path(__file__).parent
PROJECT_ROOT = BASE_PATH.parent.parent
MANIFEST_PATH = PROJECT_ROOT / "static/table.manifest.json"
BASE_HTML_PATH = BASE_PATH / "index_base.html"
OUTPUT_PATH = PROJECT_ROOT / "index.html"

def build_index():
    """Generate index.html from base template and manifest"""
    with BASE_HTML_PATH.open("r", encoding="utf-8") as f:
        base_html = f.read()

    with MANIFEST_PATH.open("r", encoding="utf-8") as f:
        manifest = json.load(f)

    nav_links = []
    for entry in manifest:
        label = entry["name"]
        href = f'pages/{entry["file"]}'
        nav_links.append(f'<a href="{href}" class="nav-link">{label}</a>')

    nav_html = '<nav style="margin: 40px 0; text-align: center;">\n' + " | \n".join(nav_links) + "\n</nav>"

    if "{{NAV_CONTENT}}" in base_html:
        final_html = base_html.replace("{{NAV_CONTENT}}", nav_html)
    else:
        final_html = base_html + "\n" + nav_html

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"✅ index.html written to: {OUTPUT_PATH}")

if __name__ == "__main__":
    build_index()