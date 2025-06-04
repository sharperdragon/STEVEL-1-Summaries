import json
from pathlib import Path

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

def get_all_medical_terms():
    global _all_terms
    if _all_terms:
        return _all_terms
    for name, path in ONTOLOGY_PATHS.items():
        _all_terms |= _load_flat_terms(path)
    return _all_terms

def is_medical_term(word: str) -> bool:
    return word.lower() in get_all_medical_terms()

def is_medical_phrase(phrase: str) -> bool:
    return any(is_medical_term(w) for w in phrase.split())