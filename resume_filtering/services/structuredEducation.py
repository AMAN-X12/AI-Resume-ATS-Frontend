
import re


DEGREE_TYPES = [
"bachelor",
"bsc",
"bs",
"b.tech",
"master",
"msc",
"ms",
"phd",
"doctorate",
"fsc",
"intermediate",
"matric"
]



def extract_years(text):
    match = re.search(r"(19|20)\d{2}\s*[-–—]\s*(19|20)\d{2}", text)
    if match:
        years = match.group()
        start, end = re.split(r"[-–—]", years)
        return start.strip(), end.strip()
    return None, None


def extract_cgpa(text):
    match = re.search(r"(cgpa|gpa)\s*[:\- ]?\s*(\d+(\.\d{1,2})?)", text.lower())
    if match:
        return match.group(2)
    return None


def extract_degree(text):
    lower = text.lower()
    for deg in DEGREE_TYPES:
        if deg in lower:
            return deg
    return None

def structure_education(education_list):
    structured = []
    for edu in education_list:
        start, end = extract_years(edu)
        cgpa = extract_cgpa(edu)
        degree = extract_degree(edu)
        entry = {
            "degree": degree,
            "start_year": start,
            "end_year": end,
            "cgpa": cgpa
        }
        structured.append(entry)
    return structured
