import json
from bs4 import BeautifulSoup
from pathlib import Path
import re

# Configurable paths
PAGES_DIR = Path("pages")
OUTPUT_FILE = Path("assets/search_index.json")

def extract_terms_from_table(table):
    terms = set()
    for row in table.find_all("tr"):
        for cell in row.find_all("td"):
            # Clean and split by non-word characters
            text = cell.get_text(separator=" ", strip=True)
            words = re.findall(r"\b[\w\-\/\+]{3,}\b", text.lower())
            terms.update(words)
    return terms

def generate_search_index():
    index = []
    for html_file in PAGES_DIR.glob("*.html"):
        soup = BeautifulSoup(html_file.read_text(encoding="utf-8"), "html.parser")
        tables = soup.find_all("table")
        if not tables:
            continue

        all_terms = set()
        for table in tables:
            all_terms.update(extract_terms_from_table(table))

        section = html_file.stem.replace("-", " ").title()
        for term in sorted(all_terms):
            index.append({
                "term": term,
                "page": html_file.name,
                "section": section
            })

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(index, indent=2))
    print(f"✅ Search index written to {OUTPUT_FILE} with {len(index)} entries.")

if __name__ == "__main__":
    generate_search_index()