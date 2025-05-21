from bs4 import BeautifulSoup

def annotate_table_columns(soup: BeautifulSoup):
    """
    Adds data-col attributes to <td> and <th> elements for column-based control.
    Injects a dropdown toggle menu into <th> headers (excluding colspans).
    """
    for row in soup.find_all("tr"):
        cells = row.find_all(["td", "th"])
        for idx, cell in enumerate(cells):
            cell["data-col"] = str(idx)

            if cell.name == "th" and not cell.has_attr("colspan"):
                clean_text = cell.get_text(strip=True)
                cell.clear()

                menu = soup.new_tag("div", **{"class": "th-menu-wrapper"})
                label = soup.new_tag("span", **{"class": "th-title"})
                label.string = clean_text

                dropdown = soup.new_tag("div", **{"class": "th-dropdown"})
                action = soup.new_tag("a", href="#", on =f"toggleColumn({idx}); return false;")
                action.string = "Hide Column"
                dropdown.append(action)

                row_action = soup.new_tag("a", href="#", onclick=f"toggleColumnRow({idx}); return false;")
                row_action.string = "Show Row Instead"
                dropdown.append(row_action)

                menu.append(label)
                menu.append(dropdown)
                cell.append(menu)


# Navigation HTML utilities
from pathlib import Path

def normalize_name(filename: str) -> str:
    return filename.replace(".table.html", "").lower()

def labelize_name(filename: str) -> str:
    name = normalize_name(filename)
    return name.replace("_", " ").title()

def generate_nav_html(current_file: Path, table_files: list[Path]) -> str:
    """Generate navigation HTML with Home link and all other tables except the current one."""
    home_link = '<div style="text-align: left;"><a href="../index.html" class="nav-link">🏠 Home</a></div>'
    other_links = []
    for other in table_files:
        if other.name == current_file.name:
            continue
        name = normalize_name(other.name)
        label = labelize_name(other.name)
        other_links.append(f'<a href="../pages/{name}.html" class="nav-link">{label}</a>')
    centered_links = '<div style="text-align: center;">' + ' | '.join(other_links) + '</div>'
    return f"<nav style='margin: 10px 0;'>\n{home_link}\n{centered_links}\n</nav>\n"