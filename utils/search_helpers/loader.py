import json
import requests
from pathlib import Path
from functools import lru_cache

HP_JSON_PATH = Path("assets/hp.json")
WORDLIST_PATH = Path("assets/wordlist.txt")
SEARCH_INDEX_PATH = Path("assets/search_index.json")

ONTOLOGY_PATHS = {
    "mesh": Path("assets/ontologies/mesh_terms.json"),
    "umls": Path("assets/ontologies/umls_terms.json"),
    "rxnorm": Path("assets/ontologies/rxnorm_terms.json"),
    "hpo": Path("assets/ontologies/hpo_terms.json"),
}

_all_terms = set()

def _load_flat_terms(path):
    try:
        return set(json.loads(path.read_text(encoding="utf-8")))
    except:
        return set()

def load_hp_terms():
    try:
        with open(HP_JSON_PATH, "r", encoding="utf-8") as f:
            return set(json.load(f))
    except Exception as e:
        return set()

def load_wordlist():
    try:
        return set(w.strip().lower() for w in WORDLIST_PATH.read_text(encoding="utf-8").splitlines() if w.strip())
    except Exception:
        return set()

def get_all_medical_terms():
    global _all_terms
    if _all_terms:
        return _all_terms
    for name, path in ONTOLOGY_PATHS.items():
        _all_terms |= _load_flat_terms(path)
    _all_terms |= load_hp_terms()
    _all_terms |= load_wordlist()
    return _all_terms

@lru_cache(maxsize=1024)
def query_umls(term: str) -> bool:
    # Placeholder — requires actual license key and ticket mechanism
    return False

@lru_cache(maxsize=1024)
def query_rxnorm(term: str) -> bool:
    try:
        resp = requests.get(
            f"https://rxnav.nlm.nih.gov/REST/approximateTerm.json",
            params={"term": term}
        )
        return "candidate" in resp.json().get("approximateGroup", {})
    except:
        return False

def is_medical_term(word: str) -> bool:
    word = word.lower()
    if word in get_all_medical_terms():
        return True
    return query_rxnorm(word) or query_umls(word)

def is_medical_phrase(phrase: str) -> bool:
    return any(is_medical_term(w) for w in phrase.split())