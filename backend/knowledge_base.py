import json
import re
from pathlib import Path
from typing import Dict, List, Tuple

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "agriculture_faq.json"

def _tokens(text: str) -> set[str]:
    # Keep Unicode letters and numbers (works for Devanagari and Bengali scripts).
    return {token for token in re.findall(r"[^\W_]+", text.lower(), flags=re.UNICODE) if len(token) > 1}

def load_faq() -> List[Dict]:
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)

def retrieve(question: str, language: str) -> Tuple[Dict | None, float]:
    entries = load_faq()
    q_tokens = _tokens(question)
    best_item, best_score = None, 0.0
    for item in entries:
        if item.get("language") != language:
            continue
        searchable = " ".join([item.get("question", ""), *item.get("keywords", [])])
        item_tokens = _tokens(searchable)
        if not q_tokens or not item_tokens:
            continue
        overlap = len(q_tokens & item_tokens)
        # Simple transparent baseline; replace with embeddings/vector search for production.
        score = overlap / max(1, len(q_tokens))
        if score > best_score:
            best_item, best_score = item, score
    return best_item, best_score
