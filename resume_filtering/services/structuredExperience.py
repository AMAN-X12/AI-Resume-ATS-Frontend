import re
from datetime import datetime

from resume_filtering.models.scapyModel import nlp
from resume_filtering.services.normalizeSKillsPipeline import normalize_skills_pipeline

ROLE_KEYWORDS = {
    "engineer", "developer", "analyst",
    "manager", "intern", "consultant",
    "scientist", "designer","architect", "lead",
    "director", "specialist", "coordinator", "officer"
}
_DATE_FORMATS = ["%b %Y", "%B %Y", "%Y", "%m/%Y"]

def extractTitle(noun_phrases):
    """Return the first noun phrase that contains a keyword from ROLE_KEYWORD."""
    for phrase in noun_phrases:
        line_lower = phrase.lower()
        if any(char.isdigit() for char in line_lower):
            continue #skips dates if any
        for keyword in ROLE_KEYWORDS:
            if keyword in line_lower:
                return " ".join(phrase.split()[:4])
    return None

def extract_entities(text):
    """Returns a dict of entities for the candidate Experience
       includes companies and the the role/title there
    """
    doc = nlp(text)
    companies = []
    for ent in doc.ents:
        if ent.label_ == "ORG":
            companies.append(ent.text)
    noun_phrases = [chunk.text for chunk in doc.noun_chunks]
    titiles= extractTitle(noun_phrases)
    return {
        "companies": list(set(companies)),
        "titles": titiles
    }

def _parse_date(date_str: str) -> datetime | None:
    """Try multiple date formats and return a datetime or None."""
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None

def datesExtraction(text):
    """Find a date-range pattern in text and return (start, end) strings."""
    pattern = r"([A-Za-z]{3,9}\s?\d{4}|\d{4})\s*[-–—]\s*(Present|[A-Za-z]{3,9}\s?\d{4}|\d{4})"
    match = re.search(pattern, text)
    if match:
        start = match.group(1)
        end = match.group(2)
        return start, end
    return None, None


def extract_experience(experience):
    """
    Convert raw experience text blocks into structured dicts
    Returns list of structured dicts
    """
    structured = []
    for exp in experience:
        if not exp.strip():
            continue
        start, end = datesExtraction(exp)
        entities = extract_entities(exp)
        entry = {
            "companies": entities["companies"],
            "titles": entities["titles"],
            "start_date": start,
            "end_date": end,
            "duration_months": calculate_duration(start, end) if start and end else None
        }
        structured.append(entry)
    return structured



def calculate_duration(start, end):
    """Return number of months between start and end dates."""
    if end.lower() in ("present", "current"):
        end_date = datetime.now()
    else:
        end_date = _parse_date(end)

    start_date = _parse_date(start)

    if start_date is None or end_date is None:
        return None

    months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    return max(months, 0)

