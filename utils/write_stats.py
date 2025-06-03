import json
from pathlib import Path
from bs4 import BeautifulSoup
from collections import defaultdict

def analyze_table_stats(table_files):
    deprecated_classes = {"table_old", "unstyled", "legacy"}

    stats = {
        "total_tables": 0,
        "tables_with_sections": 0,
        "tables_with_no_class": 0,
        "tables_with_multiple_classes": 0,
        "tables_with_deprecated_class": 0,
        "class_counts": defaultdict(int),
        "file_classes": {},
        "class_usage_per_file": defaultdict(lambda: defaultdict(int)),
        "unique_classes": [],
        "total_rows": 0,
        "total_cols": 0,
        "tables_with_header_row": 0,
        "tables_with_span": 0,
    }

    for table_file in table_files:
        soup = BeautifulSoup(table_file.read_text(), "html.parser")
        tables = soup.find_all("table")
        stats["total_tables"] += len(tables)

        for t in tables:
            rows = t.find_all("tr")
            stats["total_rows"] += len(rows)

            if any(cell.name == "th" for row in rows for cell in row.find_all(["th", "td"])):
                stats["tables_with_header_row"] += 1

            if any(cell.has_attr("colspan") or cell.has_attr("rowspan") for row in rows for cell in row.find_all(["td", "th"])):
                stats["tables_with_span"] += 1

            # estimate columns from the first row
            if rows:
                first_row_cells = rows[0].find_all(["td", "th"])
                stats["total_cols"] += len(first_row_cells)

            cls = t.get("class", [])
            if not cls:
                stats["tables_with_no_class"] += 1
            if len(cls) > 1:
                stats["tables_with_multiple_classes"] += 1
            if any(c in deprecated_classes for c in cls):
                stats["tables_with_deprecated_class"] += 1
            # Detect tables with section rows: at least one <td class="row-divider"> in the table
            if any("row-divider" in td.get("class", []) for td in t.find_all("td")):
                stats["tables_with_sections"] += 1
            for c in cls:
                stats["class_counts"][c] += 1
                stats["class_usage_per_file"][table_file.name][c] += 1

            stats["file_classes"][table_file.name] = cls

    # Group class names by prefix and sort alphabetically within each group
    import re
    grouped_counts = defaultdict(lambda: defaultdict(dict))
    class_file_map = defaultdict(list)

    for fname, classes in stats["file_classes"].items():
        for c in classes:
            class_file_map[c].append(fname)

    for class_name, count in stats["class_counts"].items():
        m = re.match(r"([a-zA-Z]+)", class_name)
        prefix = m.group(1) if m else "other"
        grouped_counts[prefix][class_name] = {
            "count": count,
            "files": sorted(class_file_map[class_name])
        }

    stats["class_counts"] = {
        group: dict(sorted(classes.items()))
        for group, classes in sorted(grouped_counts.items())
    }

    stats["unique_classes"] = sorted(
        k for g in stats["class_counts"] for k in stats["class_counts"][g]
    )

    stats["file_classes"] = {
        fname: sorted(classes) for fname, classes in sorted(stats["file_classes"].items())
    }

    # Remove unused key
    stats.pop("class_usage_per_file", None)

    if stats["total_tables"] > 0:
        stats["avg_rows_per_table"] = round(stats["total_rows"] / stats["total_tables"], 2)
        stats["avg_cols_per_table"] = round(stats["total_cols"] / stats["total_tables"], 2)

    return stats

def write_if_changed(path, content):
    if not path.exists() or path.read_text() != content:
        path.write_text(content)

def write_them_stats():
    table_dir = Path("subdex")
    table_files = list(table_dir.glob("*.table.html"))
    stats = analyze_table_stats(table_files)

    stats_path = Path("table_stats.json")
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    write_if_changed(stats_path, json.dumps(stats, indent=2))
    print(f"📊 Stats file written to: {stats_path}")

if __name__ == "__main__":
    write_them_stats()
