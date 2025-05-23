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



