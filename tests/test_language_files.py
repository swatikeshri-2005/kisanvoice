import json  # noqa: I001
from pathlib import Path

def test_faq_contains_both_languages():
    path = Path(__file__).resolve().parent.parent / "data" / "agriculture_faq.json"
    items = json.loads(path.read_text(encoding="utf-8"))
    languages = {item["language"] for item in items}
    assert {"hi", "bn"}.issubset(languages)
