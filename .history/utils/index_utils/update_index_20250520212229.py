from pathlib import Path
import json
from datetime import datetime

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

    # Sort manifest entries by name
    manifest_sorted = sorted(manifest, key=lambda x: x["name"])

    nav_links = []
    summary_cards = []
    for entry in manifest_sorted:
        label = entry["name"]
        href = f'pages/{entry["file"]}'
        nav_links.append(f'<a href="{href}" class="nav-link">{label}</a>')
        summary_cards.append(f'<div class="summary-card"><a href="{href}">{label}</a></div>')

    nav_html = '<nav style="margin: 40px 0; text-align: center;">\n' + " | \n".join(nav_links) + "\n</nav>"
    summary_html = "\n".join(summary_cards)

    buzzword_file = BASE_ / "assets/buzzwords.txt"
    buzzwords = ""
    
if buzzword_file.exists():
    buzzwords = buzzword_file.read_text(encoding="utf-8").strip().replace("\n", "  ")

base_html = base_html.replace("{{BUZZWORDS}}", buzzwords)

    last_updated = datetime.now()
    formatted_date = last_updated.strftime("%B %d")
    last_updated_html = f'<time datetime="{last_updated.date()}">{formatted_date}</time>'

    final_html = base_html
    final_html = final_html.replace("{{NAV_CONTENT}}", nav_html)
    final_html = final_html.replace("{{SUMMARY_CARDS}}", summary_html)
    final_html = final_html.replace("{{LAST_UPDATED}}", last_updated_html)

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"✅ index.html written to: {OUTPUT_PATH}")

if __name__ == "__main__":
    build_index()