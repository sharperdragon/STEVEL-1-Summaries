import json
from pathlib import Path
def convert_buzzwords_to_json(
    input_path=Path("utils/Texts/buzzwords.txt"),
    output_path=Path("utils/Texts/buzzwords.json"),
    verbose=True,
):
    buzzwords = {}

    with input_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "=" not in line:
                continue
            term, assoc = map(str.strip, line.split("=", 1))
            buzzwords[term] = assoc

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(buzzwords, f, indent=2, ensure_ascii=False)

    if verbose:
        print(f"✅ Converted {len(buzzwords)} buzzwords to key-value JSON.")