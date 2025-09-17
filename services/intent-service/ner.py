import spacy
import re
from datetime import datetime

nlp = spacy.load("en_core_web_sm")

ORDER_ID_PATTERN = re.compile(r"\b\d{5}\b")
DATE_PATTERNS = [
    r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",
    r"\b\d{4}-\d{2}-\d{2}\b",
    r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2},?\s+\d{2,4}\b",
]

def is_date(text: str) -> bool:
    """Check if text looks like a date."""
    for pat in DATE_PATTERNS:
        if re.search(pat, text, flags=re.IGNORECASE):
            return True
    try:
        _ = datetime.strptime(text, "%Y-%m-%d")
        return True
    except Exception:
        return False

def extract_entities(text: str) -> dict:
    doc = nlp(text)
    entities = {}

    for ent in doc.ents:
        if ORDER_ID_PATTERN.fullmatch(ent.text.strip()):
            entities.setdefault("order_id", []).append(ent.text)

        elif ent.label_ in ["DATE", "TIME"] or is_date(ent.text):
            entities.setdefault("order_date", []).append(ent.text)

        elif ent.text.lower().startswith("order"):
            entities.setdefault("order", []).append(ent.text)

        elif ent.label_ == "PRODUCT":
            entities.setdefault("product_name", []).append(ent.text)

        else:
            entities.setdefault(ent.label_.lower(), []).append(ent.text)

    return entities