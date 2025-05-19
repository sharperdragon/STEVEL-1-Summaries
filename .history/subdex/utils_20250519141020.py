
# New postprocessing script: apply_quiz_classes.py
from bs4 import BeautifulSoup

files = list(TABLE_DIR.glob("*.table.html"))

for path in files:
    soup = BeautifulSoup(path.read_text(), "html.parser")
    modified = False

    for td in soup.find_all("td"):
        if "quiz-answer" not in td.get("class", []) and td.find("ul"):
            td["class"] = td.get("class", []) + ["quiz-answer"]
            modified = True

    if modified:
        path.write_text(str(soup))
        print(f"✅ Updated: {path.name}")
    else:
        print(f"➖ No change: {path.name}")