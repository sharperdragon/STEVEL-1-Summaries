from bs4 import BeautifulSoup
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
    card_descriptions = {
        "Metabolism": "Includes glycolysis, glycogen storage, and fatty acid oxidation disorders.",
        "Hemeonc": "Summarizes hematologic malignancies, anemias, and blood-related findings.",
        "Chromosomes": "Genetic disorders and syndromes organized by chromosome number.",
        "Autoantibodies": "Autoimmune diseases and their associated antibodies for diagnosis.",
        "Rapid Associations": "Rapid-fire 'most common' and high-yield Step 1 associations."
    }
    for entry in manifest_sorted:
        label = entry["name"]
        href = f'pages/{entry["file"]}'
        nav_links.append(f'<a href="{href}" class="nav-link">{label}</a>')
        desc = card_descriptions.get(label, f"A high-yield summary table for {label.lower()}.")
        summary_cards.append(
            f'''<a class="summary-card" href="{href}">
  <div class="card-title">{label}</div>
  <div class="card-desc">{desc}</div>
</a>'''
        )

    nav_html = '<nav style="margin: 40px 0; text-align: center;">\n' + " | \n".join(nav_links) + "\n</nav>"
    summary_html = "\n".join(summary_cards)

    buzzword_file = BASE_PATH / "Texts/buzzwords.txt"
    buzzwords = ""
    
    if buzzword_file.exists():
        buzzwords = buzzword_file.read_text(encoding="utf-8").strip().replace("\n", "  ")


    def extract_rr_associations_html():
        rr_path = PROJECT_ROOT / "subdex/rapid_associations.table.html"
        if not rr_path.exists():
            return "<!-- Rapid Review data not found -->"

        soup = BeautifulSoup(rr_path.read_text(encoding="utf-8"), "html.parser")
        rows = soup.select("tbody tr")
        items = []
        for row in rows:
            cells = row.find_all("td")
            if len(cells) == 2:
                q = cells[0].get_text(strip=True)
                a = cells[1].get_text(strip=True)
                items.append(f'<div class="carousel-item"><div class="question">{q}</div><div class="answer">{a}</div></div>')

        return '<div class="carousel-container">' + "\n".join(items) + '</div>'

    carousel_html = extract_rr_associations_html()

    base_html = base_html.replace("{{BUZZWORDS}}", buzzwords)

    last_updated = datetime.now()
    formatted_date = last_updated.strftime("%B %d")
    last_updated_html = f'<time datetime="{last_updated.date()}">{formatted_date}</time>'

    final_html = base_html
    final_html = final_html.replace("{{NAV_CONTENT}}", nav_html)
    final_html = final_html.replace("{{SUMMARY_CARDS}}", summary_html)
    final_html = final_html.replace("{{RAPID_REVIEW_CAROUSEL}}", carousel_html)
    final_html = final_html.replace("{{LAST_UPDATED}}", last_updated_html)

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        f.write(final_html)

    print(f"✅ index.html written to: {OUTPUT_PATH}")

if __name__ == "__main__":
    build_index()