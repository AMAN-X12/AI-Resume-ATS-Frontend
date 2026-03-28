An AI-based Applicant Tracking System (ATS) backend that processes, parses, and scores candidate resumes against job requirements using Natural Language Processing (NLP) and vector embeddings.

This repository contains the FastAPI server, MongoDB data management (using session IDs to keep candidate data secure and isolated during API calls), and the Dockerized AI pipeline. It is designed to make resume screening effortless for HR teams and industries by using AI to generate clear, detailed candidate evaluations.

 This backend is highly decoupled from the frontend. You can find the frontend interface in the repository "AI Resume Frontend".Additionaly Documentation Strings (DOC Strings) are also provided in functions where i think there's a need. 

 For the live demo , kindly do visit the "AI Resume Frontend" repository you will gonna find the link of live demo there.

##  Features & Output
The API returns real-time JSON data for the UI (Name, Email, Skill Score, Experience Score, Weighted Score) and dynamically generates a highly detailed Excel report.

The Excel sheet provides a dedicated column for:
* Name, Email, and Phone
* Extracted Skills and Projects
* Skill Score, Experience Score, and Total Weighted Score
* Total Experience (in months)
* Individual work experiences (Role, Company, Duration in months)
* Education and Certifications
* Languages
* Required Job Skills and Experience (for reference)

This makes it incredibly easy for recruiters to review, sort, and filter candidate data offline.

## Project structure

```
ResumeFilter/
├── main.py                     ← FastAPI app
├── Dockerfile
├── .env
├── .gitignore
├── requirements.txt
└── resume_filtering/
    ├── models/
    │   ├── embeddingsModel.py               ← SentenceTransformer loader
    │   └── spacyModel.py                    ← spaCy NLP loader
    └── services/
        ├── resume_parser.py                 ← PDF text extraction + OCR fallback
        ├── segmentation.py                  ← Section detection (Skills, Experience, etc.)
        ├── informationExtractor.py          ← Name, email, phone, skills, experience…
        ├── normalizeSKillsPipeline.py       ← Skill normalization via clustering
        ├── similarityChecking.py            ← Cosine similarity + eligibility verdict
        ├── structuredExperience.py          ← Structured experience extraction
        ├── structuredEducation.py           ← Structured education extraction
        ├── jobpipeline.py                   ← Job requirement processing
        └── embeddingsGenerator.py           ← Embedding generation wrapper
```

---

## Setup

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. Install spaCy English model

```bash
python -m spacy download en_core_web_sm
```

### 3. Install Tesseract OCR (for scanned PDF support)

- **macOS:** `brew install tesseract`
- **Windows:** Download from https://github.com/UB-Mannheim/tesseract/wiki
  - After installing, either add to PATH or set env var: `TESSERACT_CMD=C:\...\tesseract.exe` - if downloaded on c drive on windows , just uncomment the line in resume_parser.py

### 4. Download NLTK data

```python
import nltk
nltk.download('punkt_tab') #(first run only) just uncomment the line where it is downlaoded when doing the very first run.
```

---

## Running the API

```bash
uvicorn main:app --reload
```
if running from main just run the main.py


API docs available at: http://localhost:8000/docs

---

## API usage

### POST /filter

**Form fields:**

| Field                | Type | Description                                           |
|----------------------|------|-------------------------------------------------------|
| `resume`             | file | PDF file of the candidate's resume                   |
| `job_skills`         | str  | Required skills, comma-separated                      |
| `required_experience`| str  | Experience requirements in plain English              |

**Example (curl):**

```bash
curl -X POST http://localhost:8000/filter \
  -F "resume=@candidate_resume.pdf" \
  -F "job_skills=Python, Machine Learning, SQL, FastAPI" \
  -F "required_experience=3 years backend development, 2 years machine learning"
```


### GET/export
 Returns a excel file from the database using the session ID of the user

### Delete/results
 clear the data from the database using the session id of the user

In Case of any changes that you find or any error that un-intentionally comes or for any improvement kindly email at (sardaramaan13@gmail.com)

