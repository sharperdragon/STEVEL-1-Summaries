from bs4 import BeautifulSoup

def annotate_table_columns(soup: BeautifulSoup):
    """
    Adds data-col attributes to <td> and <th> elements for column-based control.
    Injects a dropdown toggle menu into <th> headers (excluding colspans).
    """
    for row in soup.find_all("tr"):
        # Apply .row-divider class to <td> with colspan outside thead
        if not row.find_parent("thead"):
            for cell in row.find_all("td"):
                if cell.has_attr("colspan"):
                    existing_classes = cell.get("class", [])
                    if "row-divider" not in existing_classes:
                        cell["class"] = existing_classes + ["row-divider"]

        cells = row.find_all(["td", "th"])
        for idx, cell in enumerate(cells):
            cell["data-col"] = str(idx)

            if cell.name == "th" and not cell.has_attr("colspan"):
                clean_text = cell.get_text(strip=True)
                cell.clear()

                parent_table = cell.find_parent("table")
                table_class = ""
                if parent_table and parent_table.has_attr("class"):
                    for cls in parent_table["class"]:
                        if cls in {"table1", "table2", "table3"}:
                            table_class = cls
                            break

                menu = soup.new_tag("div", **{"class": "th-menu-wrapper"})
                label = soup.new_tag("span", **{"class": "th-title"})
                label.string = clean_text

                dropdown = soup.new_tag("div", **{"class": "th-dropdown", "display": "none"})
                action = soup.new_tag("a", href="#", onclick=f"toggleColumn({idx}); return false;")
                action["class"] = "col-toggle"
                action.string = "Hide Column"
                dropdown.append(action)


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
    other_links = []
    for other in table_files:
        if other.name == current_file.name:
            continue
        name = normalize_name(other.name)
        label = labelize_name(other.name)
        other_links.append(f'<a href="../pages/{name}.html" class="nav-link">{label}</a>')
    centered_links = '<div style="text-align: center;">' + ' | '.join(other_links) + '</div>'
    return f"<nav style='margin: 10px 0;'>\n{centered_links}\n</nav>\n"
def remove_row_dividers(soup: BeautifulSoup):
    """
    Removes all <tr> elements with class 'row-divider' from the soup.
    """
    for tr in soup.find_all("tr", class_="row-divider"):
        tr.decompose()