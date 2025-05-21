import os
import json
from pathlib import Path
from bs4 import BeautifulSoup
from utils.index_utils.update_index import build_index
from utils.html_utils import (
    annotate_table_columns,
    generate_nav_html,
    normalize_name,
    labelize_name,
)
from utils.Texts.buzzword_json_builder import convert_buzzwords_to_json
from datetime import datetime

BASE_HTML_PATH = Path("pages/BASE.html")
TABLE_DIR = Path("subdex/")
NAV_DIR = Path("utils/navs/")
OUTPUT_DIR = Path("pages/")
MANIFEST_PATH = Path("static/data/table.manifest.json")

TABLE_SUFFIX = ".table.html"

"""Module to update HTML pages by processing table files, annotating columns for toggling, generating navigation bars, and building a manifest."""

def write_if_changed(path: Path, content: str):
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.write_text(content, encoding="utf-8")
    return True

def extract_rr_associations_html(items):
    """
    Given a list of HTML strings representing rapid associations, returns
    a carousel container where only the first item is visible on page load.
    """
    html = ['<div class="carousel-container">']
    for i, item in enumerate(items):
        if i == 0:
            item_visible = item.replace('class="answer"', 'class="answer" style="display:none;"')
            html.append(item_visible)
        else:
            item_hidden = item.replace('class="carousel-item"', 'class="carousel-item" style="display:none;"')
            item_hidden = item_hidden.replace('class="answer"', 'class="answer" style="display:none;"')
            html.append(item_hidden)
    html.append("</div>")
    return "\n".join(html)

def build_all():
    """
    Main function to build all HTML pages from table files.
    Processes tables, annotates columns for toggling, generates navigation bars,
    writes output HTML files, and updates the manifest.
    """
    # Ensure output and navigation directories exist
    OUTPUT_DIR.mkdir(exist_ok=True)
    NAV_DIR.mkdir(parents=True, exist_ok=True)

    manifest = []
    card_manifest = []
    base_html = BASE_HTML_PATH.read_text()
    # The base HTML must include {{PAGE_TITLE}}, {{NAV_CONTENT}}, and {{TABLE_CONTENT}} placeholders
    required_placeholders = ["{{PAGE_TITLE}}", "{{NAV_CONTENT}}", "{{TABLE_CONTENT}}"]
    missing = [ph for ph in required_placeholders if ph not in base_html]
    if missing:
        raise ValueError(f"❌ Missing required placeholder(s) in BASE.html: {', '.join(missing)}")

    # Gather all table files to process
    table_files_all = sorted(TABLE_DIR.glob("*"))
    table_files = [f for f in table_files_all if f.name.endswith(TABLE_SUFFIX)]

    # Loop over each table file to build individual pages
    for table_file in table_files:
        name = normalize_name(table_file.name)
        # Force specific title formats for certain table types
        if "HLA" in table_file.name:
            label = labelize_name(table_file.name).upper()
        elif "CD-markers" in table_file.name:
            label = "CD Markers"
        else:
            label = labelize_name(table_file.name)

        # Load and parse table HTML content
        soup = BeautifulSoup(table_file.read_text(), "html.parser")

        # Annotate table columns and insert toggle buttons
        annotate_table_columns(soup)

        table_html = str(soup)

        print(f"📄 Processing: {table_file.name}")

        # Build improved navigation bar with Home and links to other pages
        nav_html = generate_nav_html(table_file, table_files)

        # Write navigation HTML to separate file for potential reuse
        nav_path = NAV_DIR / f"nav_{name}.html"
        write_if_changed(nav_path, nav_html)

        # Compose final HTML by replacing placeholders in base template
        final_html = (
            base_html
            .replace("{{PAGE_TITLE}}", label)
            .replace("{{NAV_CONTENT}}", nav_html)
            .replace("{{TABLE_CONTENT}}", table_html)
        )

        # Write the generated HTML page to output directory
        output_file = OUTPUT_DIR / f"{name}.html"
        write_if_changed(output_file, final_html)
        print(f"📄 Built page: {output_file.name}")

        # Append page info to manifest list
        manifest.append({
            "name": label,
            "file": f"{name}.html"
        })

        card_manifest.append({
            "name": label,
            "file": f"{name}.html",
            "desc": f"A high-yield summary table for {label.lower()}."  # Placeholder, can be customized later
        })

    # Ensure manifest parent directories exist
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    # Write the manifest JSON file with all pages info
    write_if_changed(MANIFEST_PATH, json.dumps(manifest, indent=2))
    print(f"\n🧾 Manifest updated: {MANIFEST_PATH}")

    card_manifest_path = Path("static/data/summary_cards.json")
    card_manifest_path.parent.mkdir(parents=True, exist_ok=True)
    write_if_changed(card_manifest_path, json.dumps(card_manifest, indent=2))
    print(f"🧾 Summary cards written to: {card_manifest_path}")

    summary = {
        "updated": datetime.now().isoformat(),
        "pages_built": [f.name for f in table_files],
        "manifest_count": len(manifest)
    }
    Path("build_summary.json").write_text(json.dumps(summary, indent=2))

if __name__ == "__main__":
    convert_buzzwords_to_json()
    build_all()
    build_index()