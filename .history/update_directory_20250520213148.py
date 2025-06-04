import os
import json
from pathlib import Path
from bs4 import BeautifulSoup
from utils.index_utils.update_index import build_index
from utils.page_helpers.html_utils import (
    annotate_table_columns,
    generate_nav_html,
    normalize_name,
    labelize_name,
)
from utils.Texts.buzzword_json_builder import convert_buzzwords_to_json


BASE_HTML_PATH = Path("pages/BASE.html")
TABLE_DIR = Path("subdex/")
NAV_DIR = Path("utils/navs/")
OUTPUT_DIR = Path("pages/")
MANIFEST_PATH = Path("static/table.manifest.json")

TABLE_SUFFIX = ".table.html"

"""Module to update HTML pages by processing table files, annotating columns for toggling, generating navigation bars, and building a manifest."""

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
    base_html = BASE_HTML_PATH.read_text()
    # The base HTML must include {{PAGE_TITLE}}, {{NAV_CONTENT}}, and {{TABLE_CONTENT}} placeholders
    required_placeholders = ["{{PAGE_TITLE}}", "{{NAV_CONTENT}}", "{{TABLE_CONTENT}}"]
    missing = [ph for ph in required_placeholders if ph not in base_html]
    if missing:
        raise ValueError(f"❌ Missing required placeholder(s) in BASE.html: {', '.join(missing)}")

    # Gather all table files to process
    table_files = sorted(TABLE_DIR.glob(f"*{TABLE_SUFFIX}"))

    # Loop over each table file to build individual pages
    for table_file in table_files:
        name = normalize_name(table_file.name)
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
        nav_path.write_text(nav_html)

        # Compose final HTML by replacing placeholders in base template
        final_html = (
            base_html
            .replace("{{PAGE_TITLE}}", label)
            .replace("{{NAV_CONTENT}}", nav_html)
            .replace("{{TABLE_CONTENT}}", table_html)
        )

        # Write the generated HTML page to output directory
        output_file = OUTPUT_DIR / f"{name}.html"
        output_file.write_text(final_html)
        print(f"📄 Built page: {output_file.name}")

        # Append page info to manifest list
        manifest.append({
            "name": label,
            "file": f"{name}.html"
        })

    # Write the manifest JSON file with all pages info
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))
    print(f"\n🧾 Manifest updated: {MANIFEST_PATH}")


if __name__ == "__main__":
    build_all()
    build_index()