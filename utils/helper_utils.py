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
    base = filename.replace(".table.html", "").lower()

    # Primary hardcoded overrides
    label_overrides = {
        "cd-markers": "CD Markers",
        "hla": "HLA",
        "lab-tests": "Labs",
        "hemeonc": "Heme-Onc"
    }

    if base in label_overrides:
        label = label_overrides[base]
    elif "cd" in base and "marker" in base:
        label = "CD Markers"
    elif "lab" in base and "test" in base:
        label = "Labs"
    elif base.startswith("rapid_"):
        label = base.replace("rapid_", "", 1).replace("_", " ").title()
    else:
        label = base.replace("_", " ").title()

    slug = label.lower().replace(" ", "-")
    return label, slug

# is safe, but if someone hardcoded label = "CD Markers" without sanitizing the input, 
# it could mismatch during category checks. You’re fine as-is given the current flow, but be aware if you ever decouple slug from label generation.

