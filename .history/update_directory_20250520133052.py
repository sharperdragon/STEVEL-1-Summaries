import os
import json
from pathlib import Path
from bs4 import BeautifulSoup

BASE_HTML_PATH = Path("subdex/Base.html")
TABLE_DIR = Path("subdex/")
NAV_DIR = Path("utils/navs/")
OUTPUT_DIR = Path("pages/")
MANIFEST_PATH = Path("static/table.manifest.json")

TABLE_SUFFIX = ".table.html"


def apply_quiz_classes(soup: BeautifulSoup) -> bool:
    """Add 'quiz-answer' class to the last <td> or <th> in every row."""
    modified = False
    for tr in soup.find_all("tr"):
        cells = tr.find_all(["td", "th"])
        if cells:
            target = cells[-1]
            if "quiz-answer" not in target.get("class", []):
                target["class"] = target.get("class", []) + ["quiz-answer"]
                modified = True
    return modified


def normalize_name(filename: str):
    return filename.replace(TABLE_SUFFIX, "")


def labelize_name(filename: str):
    return normalize_name(filename).replace("_", " ").replace("-", " ").title()


def build_all():
    OUTPUT_DIR.mkdir(exist_ok=True)
    NAV_DIR.mkdir(parents=True, exist_ok=True)

    manifest = []
    base_html = BASE_HTML_PATH.read_text()

    table_files = sorted(TABLE_DIR.glob(f"*{TABLE_SUFFIX}"))

    for table_file in table_files:
        name = normalize_name(table_file.name)
        label = labelize_name(table_file.name)

        # Load and mutate table HTML
        soup = BeautifulSoup(table_file.read_text(), "html.parser")
        modified = apply_quiz_classes(soup)
        table_html = str(soup)

        if modified:
            table_file.write_text(table_html)
            print(f"🔁 Updated quiz-classes in: {table_file.name}")
        else:
            print(f"✅ No change needed: {table_file.name}")

        # Build navigation bar
        nav_links = ['  <a href="../index.html" class="nav-link"> HOME </a> |']
        for other in table_files:
            if other == table_file:
                continue
            other_name = normalize_name(other.name)
            other_label = labelize_name(other.name)
            nav_links.append(f'  <a href="../pages/{other_name}.html" class="nav-link">{other_label}</a> |')
        nav_html = "<nav style='margin: 10px 0; text-align: center;'>\n" + "\n".join(nav_links) + "\n</nav>\n"

        nav_path = NAV_DIR / f"nav_{name}.html"
        nav_path.write_text(nav_html)

        # Inject into base template
        final_html = (
            base_html
            .replace("{{PAGE_TITLE}}", label)
            .replace("{{NAV_CONTENT}}", nav_html)
            .replace("{{TABLE_CONTENT}}", table_html)
        )

        output_file = OUTPUT_DIR / f"{name}.html"
        output_file.write_text(final_html)
        print(f"📄 Built page: {output_file.name}")

        manifest.append({
            "name": label,
            "file": f"{name}.html"
        })

    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))
    print(f"\n🧾 Manifest updated: {MANIFEST_PATH}")


def update_index_page():
    """Update the index.html to include up-to-date navigation."""
    index_path = Path("index.html")
    nav_placeholder = "{{NAV_CONTENT}}"
    base_template = BASE_HTML_PATH.read_text()

    table_files = sorted(TABLE_DIR.glob(f"*{TABLE_SUFFIX}"))
    nav_links = []
    for table_file in table_files:
        name = normalize_name(table_file.name)
        label = labelize_name(table_file.name)
        nav_links.append(f'  <a href="pages/{name}.html" class="nav-link">{label}</a> |')

    nav_html = "<nav style='margin: 10px 0; text-align: center;'>\n" + "\n".join(nav_links) + "\n</nav>\n"

    if nav_placeholder in base_template:
        updated_html = base_template.replace("{{NAV_CONTENT}}", nav_html)
    else:
        updated_html = nav_html + base_template  # fallback if no placeholder

    index_path.write_text(updated_html)
    print(f"🏠 Index page updated with navigation: {index_path}")


if __name__ == "__main__":
    build_all()
    update_index_page()