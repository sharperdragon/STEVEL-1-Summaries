import os
import json
from pathlib import Path
from bs4 import BeautifulSoup
from utils.index_utils.update_index import build_index

# JS for toggling table columns
TOGGLE_SCRIPT = """
<script>
function toggleColumn(colIndex) {
  document.querySelectorAll('[data-col="' + colIndex + '"]').forEach(el => {
    el.style.display = (el.style.display === 'none') ? '' : 'none';
  });
}
</script>
"""

BASE_HTML_PATH = Path("pages/BASE.html")
TABLE_DIR = Path("subdex/")
NAV_DIR = Path("utils/navs/")
OUTPUT_DIR = Path("pages/")
MANIFEST_PATH = Path("static/table.manifest.json")

TABLE_SUFFIX = ".table.html"


def normalize_name(filename: str):
    return filename.replace(TABLE_SUFFIX, "")


def labelize_name(filename: str):
    return normalize_name(filename).replace("_", " ").replace("-", " ").title()


def build_all():
    OUTPUT_DIR.mkdir(exist_ok=True)
    NAV_DIR.mkdir(parents=True, exist_ok=True)

    manifest = []
    base_html = BASE_HTML_PATH.read_text()
    # The base HTML must include {{PAGE_TITLE}}, {{NAV_CONTENT}}, and {{TABLE_CONTENT}} placeholders

    table_files = sorted(TABLE_DIR.glob(f"*{TABLE_SUFFIX}"))

    for table_file in table_files:
        name = normalize_name(table_file.name)
        label = labelize_name(table_file.name)

        # Load and mutate table HTML
        soup = BeautifulSoup(table_file.read_text(), "html.parser")

        # Annotate each <td> and <th> with data-col index for column toggle
        for row in soup.find_all("tr"):
            cells = row.find_all(["td", "th"])
            for idx, cell in enumerate(cells):
                cell["data-col"] = str(idx)
                if cell.name == "th":
                    # Insert hide toggle button
                    button = soup.new_tag("button", **{
                        "class": "hide-col-btn",
                        "onclick": f"toggleColumn({idx})"
                    })
                    button.string = "✖"
                    cell.insert(0, button)

        table_html = str(soup)

        print(f"📄 Processing: {table_file.name}")

        # Build improved navigation bar
        home_link = '<div style="text-align: left;"><a href="../index.html" class="nav-link">🏠 Home</a></div>'
        other_links = []
        for other in table_files:
            if other.name == table_file.name:
                continue
            other_name = normalize_name(other.name)
            other_label = labelize_name(other.name)
            other_links.append(f'<a href="../pages/{other_name}.html" class="nav-link">{other_label}</a>')
        centered_links = '<div style="text-align: center;">' + ' | '.join(other_links) + '</div>'
        nav_html = f"<nav style='margin: 10px 0;'>\n{home_link}\n{centered_links}\n</nav>\n"

        nav_path = NAV_DIR / f"nav_{name}.html"
        nav_path.write_text(nav_html)

        final_html = (
            base_html
            .replace("{{PAGE_TITLE}}", label)
            .replace("{{NAV_CONTENT}}", nav_html)
            .replace("{{TABLE_CONTENT}}", table_html)
            + TOGGLE_SCRIPT
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


if __name__ == "__main__":
    build_all()
    build_index()