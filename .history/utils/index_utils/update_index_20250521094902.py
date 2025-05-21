from bs4 import BeautifulSoup
from pathlib import Path
import json
from datetime import datetime

BASE_PATH = Path(__file__).parent
PROJECT_ROOT = BASE_PATH.parent.parent
MANIFEST_PATH = PROJECT_ROOT / "static/table.manifest.json"
BASE_HTML_PATH = BASE_PATH / "index_base.html"
OUTPUT_PATH = PROJECT_ROOT / "index.html"

def write_rapid_cards_json():
    sources = {
        "presentation": PROJECT_ROOT / "subdex/rapid_presentation.table.html",
        "finding": PROJECT_ROOT / "subdex/rapid_findings.table.html",
        "association": PROJECT_ROOT / "subdex/rapid_associations.table.html"
    }

    all_items = []
    for source_label, path in sources.items():
        if not path.exists():
            continue
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        rows = soup.select("tbody tr")
        for row in rows:
            cells = row.find_all("td")
            if len(cells) != 2:
                continue
            q = cells[0].get_text(strip=True)
            a = cells[1].get_text(strip=True)
            all_items.append({
                "question": q,
                "answer": a,
                "source": source_label
            })

    output_path = PROJECT_ROOT / "static/data/rapid_cards.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Skip write if contents are unchanged
    existing = None
    if output_path.exists():
        try:
            existing = json.loads(output_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    if existing != all_items:
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(all_items, f, ensure_ascii=False, indent=2)
        print(f"📦 rapid_cards.json updated with {len(all_items)} entries.")
    else:
        print("🔁 rapid_cards.json unchanged.")

def build_index(build_json=True):
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


    carousel_html = '<div id="RapidCarousel" class="carousel-wrapper"></div>'
    if build_json:
        write_rapid_cards_json()

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