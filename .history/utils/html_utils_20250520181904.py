


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
                action = soup.new_tag("a", href="#", onclick=f"toggleColumn({idx}); return false;")
                action.string = "▼"
                dropdown.append(action)

                menu.append(label)
                menu.append(dropdown)
                cell.append(menu)