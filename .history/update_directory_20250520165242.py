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
    # The base HTML must include {{PAGE_TITLE}}, {{NAV_CONTENT}}, and {{TABLE_CONTENT}} placeholders

    table_files = sorted(TABLE_DIR.glob(f"*{TABLE_SUFFIX}"))

    for table_file in table_files:
        name = normalize_name(table_file.name)
        label = labelize_name(table_file.name)

        # Load and mutate table HTML
        soup = BeautifulSoup(table_file.read_text(), "html.parser")
        modified = apply_quiz_classes(soup)

        # Annotate each <td> cell with data-col index for column toggle
        for row in soup.find_all("tr"):
            tds = row.find_all("td")
            for idx, cell in enumerate(tds):
                cell["data-col"] = str(idx)

        # Insert hide buttons in column headers
        for th in soup.find_all("th"):
            idx = th.get("data-col")
            menu_wrapper = soup.new_tag("div", **{"class": "th-hover-menu"})
            toggle_link = soup.new_tag("a", href="#", onclick=f"toggleColumn({idx}); return false;", **{"class": "th-toggle-link"})
            toggle_link.string = "Toggle"
            while th.contents:
                menu_wrapper.append(th.contents[0])
            menu_wrapper.append(toggle_link)
            th.clear()
            th.append(menu_wrapper)

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