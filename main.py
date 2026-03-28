

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from resume_filtering.api.routes import router as resume_router

app = FastAPI(
    title="AI Resume Filter",
    description="ATS-powered resume screening system. Upload a PDF resume, provide job requirements, get an eligibility verdict."

)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(resume_router, tags=["Resume Analysis"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)