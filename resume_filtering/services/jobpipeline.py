import re
from resume_filtering.services.normalizeSKillsPipeline import normalize_skills_pipeline
from resume_filtering.models.scapyModel import nlp


def extract_jobPhrases(text):
    """Split a comma/and/or-separated skills string into individual phrases."""
    pattern = r'\s*(?:,|\band\b|\bor\b)\s*'
    skillsText= re.split(pattern, text)
    skills= [s.strip().lower() for s in skillsText]
    return skills

def extractJobRole(text):
    """
    Parse an experience requirements string like:
      '3 years backend development, 2 years in machine learning'
    into a list of:
      [{"role": ["backend development"], "experienceDuration": 36},]
    """
    pattern = r'\s*,\s*|\s*\band\b\s*'
    jobText=re.split(pattern,text)
    listOfRoles=[]
    for line in jobText:
        months=experiencemonths(line)
        line = re.sub(r'\d+\s*\+?\s*(years?|yrs?|months?|mos?)', '', line, flags=re.IGNORECASE).strip()
        line = re.sub(r'^(in|of|experience|as a|as)\s+', '', line, flags=re.IGNORECASE).strip()
        doc = nlp(line)
        role_phrases = [chunk.text for chunk in doc.noun_chunks]
        if not role_phrases and line:
            role_phrases=[line]
        listOfRoles.append({
            "role":role_phrases,
            "experienceDuration":months
        })
    return listOfRoles


def experiencemonths(text):
    """Convert 'X years' / 'X months' in text to total months."""
    pattern = r'(\d+)\s*\+?\s*(years?|yrs?|months?|mos?)'
    matches = re.findall(pattern, text.lower())
    total_months = 0
    for value, unit in matches:
        value = int(value)
        if "y" in unit:
            total_months += value * 12
        else:
            total_months += value
    return total_months

def job_pipeline(jobText,experienceText):
    """
    Process raw job requirement strings into normalized skills + role dicts.
    Returns:
        normalized_job_phrases: list of canonical skill names
        roles: list of {role: [...], experienceDuration: int}
    """
    job_phrases = extract_jobPhrases(jobText)
    nomalizedJobPhrases = normalize_skills_pipeline(job_phrases)
    roles = extractJobRole(experienceText)
    return  nomalizedJobPhrases,roles

