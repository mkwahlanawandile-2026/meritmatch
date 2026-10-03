import os
from typing import Any, Dict

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from src.extractor import extract_text
from src.matcher import run_matching_pipeline
from src.nlp_parser import parse_resume


app = FastAPI(
    title="MeritMatch API",
    description="API bridge for the MeritMatch candidate intelligence engine.",
    version="0.1.0",
)

# Allow the React frontend to communicate with FastAPI.
# Local development remains supported by default.
allowed_origins = [
    origin.strip()
    for origin in os.getenv(
        "MERITMATCH_ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",")
    if origin.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "service": "MeritMatch API",
        "version": "0.1.0",
    }


@app.post("/api/resumes/parse")
async def parse_resume_endpoint(
    file: UploadFile = File(...),
) -> Dict[str, Any]:
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="A resume file is required.",
        )

    allowed_extensions = {".pdf", ".docx", ".txt"}
    filename = file.filename.lower()

    if not any(filename.endswith(ext) for ext in allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail="Supported resume formats are PDF, DOCX, and TXT.",
        )

    try:
        from io import BytesIO

        contents = await file.read()

        upload = BytesIO(contents)
        upload.name = file.filename

        text = extract_text(upload)

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="No readable text was found in the uploaded resume.",
            )

        profile = parse_resume(text)

        return {
            "filename": file.filename,
            "profile": profile,
        }

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Resume processing failed: {exc}",
        ) from exc


@app.post("/api/match")
async def match_candidate(payload: Dict[str, Any]) -> Dict[str, Any]:
    candidate_profile = payload.get("candidate_profile")
    job_requirements = payload.get("job_requirements")

    if not isinstance(candidate_profile, dict):
        raise HTTPException(
            status_code=400,
            detail="candidate_profile must be an object.",
        )

    if not isinstance(job_requirements, dict):
        raise HTTPException(
            status_code=400,
            detail="job_requirements must be an object.",
        )

    try:
        result = run_matching_pipeline(
            candidate_profile,
            job_requirements,
        )

        return result

    except (TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Matching pipeline failed: {exc}",
        ) from exc
