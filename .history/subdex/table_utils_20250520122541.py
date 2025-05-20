
def add_quiz_answer_classes(table_dir="subdex/"):
    table_dir = Path(table_dir)
    files = list(table_dir.glob("*.table.html"))

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

if __name__ == "__main__":
    add_quiz_answer_classes()