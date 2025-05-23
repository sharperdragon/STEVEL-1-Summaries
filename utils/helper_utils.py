import os
import json
from pathlib import Path
from bs4 import BeautifulSoup



BASE_HTML_PATH = Path("pages/BASE.html")
TABLE_DIR = Path("subdex/")
NAV_DIR = Path("utils/navs/")
OUTPUT_DIR = Path("pages/")
MANIFEST_PATH = Path("static/data/table.manifest.json")

TABLE_SUFFIX = ".table.html"

table_files_all = sorted(TABLE_DIR.glob("*"))
table_files = [f for f in table_files_all if f.name.endswith(TABLE_SUFFIX)]

def generate_label_and_slug(filename: str) -> tuple[str, str]:
    base = filename.replace(".table.html", "")
    if "HLA" in base:
        label = base.upper()
    elif "CD-markers" in base:
        label = "CD Markers"
    elif "Hemeonc" in base:
        label = "Heme-Onc"
    elif base.startswith("rapid_"):
        label = base.replace("rapid_", "", 1).replace("_", " ").title()
    else:
        label = base.replace("_", " ").title()
    slug = label.lower().replace(" ", "-")
    return label, slug


def generate_drop_nav_html():
    """
    Generates a categorized dropdown-style nav with grouped sections and writes one per table
    into utils/navs/drop_navs/drop_nav_<slug>.html.
    """
    drop_nav_dir = Path("utils/navs/drop_navs")
    drop_nav_dir.mkdir(parents=True, exist_ok=True)

    table_files = sorted(TABLE_DIR.glob(f"*{TABLE_SUFFIX}"))

    def categorize(slug: str) -> str:
        if slug == "glossary":
            return "Glossary"
        elif "rapid" in slug:
            return "Rapid Review"
        elif any(x in slug for x in ["hla", "cytokine", "autoantibodies", "cd"]):
            return "Immune"
        elif any(x in slug for x in ["cardio", "respiratory", "embryo"]):
            return "System"
        else:
            return "Misc"

    for table_file in table_files:
        filename = table_file.name
        label, slug = generate_label_and_slug(filename)

        # Build category → links map
        category_map = {}
        for other_file in table_files:
            other_label, other_slug = generate_label_and_slug(other_file.name)
            if other_slug == slug:
                continue  # Skip the current page
            category = categorize(other_slug)
            category_map.setdefault(category, []).append((other_label, other_slug))

        # Build HTML
        nav_html = f'''
<nav id="float-nav-container">
    <span>Navigate</span>
    <div class="nav_dropdown_container">
'''

        for category, links in sorted(category_map.items()):
            if category == "Glossary":
                for label, link_slug in sorted(links):
                    nav_html += f'''      <a class="nav_link_tab" href="../pages/{link_slug}.html">{label}</a>\n'''
            else:
                nav_html += f'''      <div class="nav_dropdown_container nav_category_title">{category}\n'''
                for label, link_slug in sorted(links):
                    nav_html += f'''        <a class="nav_link_tab" href="../pages/{link_slug}.html">{label}</a>\n'''
                nav_html += "      </div>\n"
        nav_html += '''    </div>
</nav>
'''

        output_path = drop_nav_dir / f"drop_nav_{slug}.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(nav_html.strip())