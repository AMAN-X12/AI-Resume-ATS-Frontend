import re
from resume_filtering.models.scapyModel import nlp




excluded_keywords = ["resume", "curriculum", "vitae", "profile", "contact", "location", "link", "page"]
def nameExtractor(text) :
    """
    Extract the candidate's full name.
    Strategy
    1. spaCy model — looks for a PERSON entity in the first ~800 chars.
    2. manual finding — scans the first 10 non-empty lines to find name
    """
    # Trying  spaCy model first
    try:
        doc = nlp(text[:800])
        for ent in doc.ents:
            if ent.label_ == "PERSON" and 1 < len(ent.text.split()) <= 5:
                return ent.text.title()
    except Exception:
        pass
    # incase we dont get name thorugh spacy
    lines = text.split("\n")
    for line in lines[:10]:
        line = line.strip()
        if not line:
            continue
        if "@" in line:
            continue
        if re.search(r"\d", line):
            continue
        if any(word in line.lower() for word in excluded_keywords):
            continue
        words = line.split()
        if 1 < len(words) <= 4 and all(w.isalpha() or w in ("-", ".") for w in words):
            return line.title()

    return None


def email_extractor(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.search(email_pattern, text)
    if emails:
        return emails.group()
    return None


def phone_extractor(text):
    phone_pattern =r"(?:(?:\+|00)\d{1,3}[\s.-]?)?(?:\(?\d{3,4}\)?[\s.-]?)?\d{3}[\s.-]?\d{4}"
    phones = re.search(phone_pattern, text)
    if phones:
        return phones.group()
    return None




def skillExtractor(segments):
    skills_text=' '
    formated_skills= []
    if "skills" in segments:
        skills_text+= segments["skills"]
    else:
        skills_text+=""
        # the thing we are doing further cleaning here is this we want to remove any character 'e' or 'o' that often comes after using ocr
        # in place of bullet points or commas in the skills section
    skills_text = re.sub(r"(?m)^\s*[eo]\s+", "", skills_text)
    skills_text = re.sub(r"[•:()\n\-]+", ",", skills_text)
    for skill in skills_text.split(","):
        skill= skill.strip()
        if skill:
            formated_skills.append(skill)

    return formated_skills

def educationExtractor(segments):
    educartion_text= ' '
    formated_education= []
    if "education" in segments:
        educartion_text+= segments["education"]
    else:
        educartion_text+=""
    educartion_text = re.sub(r",",' ', educartion_text)
    for edu in educartion_text.split("\n"):
        edu= edu.strip()
        if edu:
            edu = re.sub(r'\s+',' ',edu)
            formated_education.append(edu)
    return formated_education

def languageExtractor(segments):
    language_text= ' '
    formated_language= []
    if "languages" in segments:
        language_text+= segments["languages"]
    else:
        language_text+=""
    language_text = re.sub(r",",' ', language_text)
    for lang in language_text.split("\n"):
        lang= lang.strip()
        if lang:
            lang = re.sub(r'\s+',' ',lang)
            formated_language.append(lang)
    return formated_language

def projectExtractor(segments):
    project_text= ' '
    formated_projects= []
    if "projects" in segments:
        project_text+= segments["projects"]
    else:
        project_text+=""
    project_text = re.sub(r",",' ', project_text)
    for proj in project_text.split("\n"):
        proj= proj.strip()
        if proj:
            proj = re.sub(r'\s+',' ',proj)
            formated_projects.append(proj)
    return formated_projects

def certificationExtractor(sections):

    cert_text = sections.get("certifications", "")
    lines = cert_text.split("\n")
    certs = []
    for line in lines:
        line = line.strip()
        if len(line) > 5:
            certs.append(line)
    return certs


def experienceExtractor(sections):
    """Return experience in blocks """
    experience_text = sections.get("experience", "")
    experiences = []
    block= experience_text.split("\n\n")
    pattern = r"(19|20)\d{2}|Present|Current"
    for block in block:
        block = block.strip()
        if block:
            experiences.append(block)
    return experiences


