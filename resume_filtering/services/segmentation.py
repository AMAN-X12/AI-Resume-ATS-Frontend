import re

SECTION_HEADERS = {
    "education":            ["education","academic background","qualification"],
    "experience":           ["experience","work experience","employment history","Work History"],
    "skills":               ["skills","technical skills","core competencies","Capabilities"],
    "projects":             ["projects","work"],
    "languages":            ["languages"],
    "certifications":       ["certifications","certificates"],
}

def segment_sections(text):
    """
    Split resume text into segments for example :
      from the raw resume text we get segment sections : skills , experience , projects etc.
    Returns a dict mapping diff same sections to a single one using SECTION_HEADERS for example :
      education , academic background and qualification to a single section named education
    """
    text_lower = text.lower()
    matches = []
    for section, keywords in SECTION_HEADERS.items():
        for keyword in keywords:
            pattern = rf"(?m)^\s*{re.escape(keyword)}[:\-\s]*"
            for match in re.finditer(pattern, text_lower):
                matches.append((match.end(),match.start(), section))
    matches.sort()
    sections = {}
    for i in range(len(matches)):
        start_pos = matches[i][0]
        section_name = matches[i][2]
        if i < len(matches) - 1:
            end_pos = matches[i+1][1]
        else:
            end_pos = len(text)
        sections[section_name] = text[start_pos:end_pos]
    return sections