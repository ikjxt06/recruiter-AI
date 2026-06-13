from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.candidate import Candidate, InterviewQuestion, JobDescription, Ranking, Resume
from app.schemas.candidate import CandidateProfile
from app.services.ai_service import ai_service
from app.services.file_text import extract_text
from app.services.matching import score_candidate
from app.services.resume_parser import parse_resume_text
from app.services.vector_store import get_lightweight_vector_store, get_vector_store

router = APIRouter()


@router.post("/upload")
async def upload_resumes(files: list[UploadFile] = File(...), db: Session = Depends(get_db)) -> dict:
    if len(files) > 500:
        raise HTTPException(status_code=400, detail="Upload limit is 500 resumes per batch")
    created = []
    for file in files:
        suffix = Path(file.filename or "").suffix.lower()
        if suffix not in {".pdf", ".docx"}:
            continue
        file_path = settings.upload_path / f"{uuid4().hex}{suffix}"
        file_path.write_bytes(await file.read())
        raw_text = extract_text(file_path, file.content_type or "")
        parsed = parse_resume_text(raw_text)
        candidate = Candidate(**parsed.asdict())
        db.add(candidate)
        db.flush()
        resume = Resume(
            candidate_id=candidate.id,
            file_name=file.filename or file_path.name,
            file_path=str(file_path),
            content_type=file.content_type or "application/octet-stream",
            raw_text=raw_text,
            parsed_json=parsed.asdict(),
        )
        db.add(resume)
        db.flush()
        try:
            get_vector_store().upsert_candidate(candidate.id, raw_text[:8000], {"name": candidate.name or "", "skills": ", ".join(candidate.skills)})
        except ImportError:
            get_lightweight_vector_store().upsert_candidate(candidate.id, raw_text[:8000], {"name": candidate.name or "", "skills": ", ".join(candidate.skills)})
        created.append(candidate.id)
    db.commit()
    return {"processed": len(created), "candidate_ids": created}


@router.get("", response_model=list[CandidateProfile])
def list_candidates(search: str | None = None, status: str | None = None, min_score: float | None = None, db: Session = Depends(get_db)):
    query = select(Candidate)
    if search:
        query = query.where(Candidate.name.ilike(f"%{search}%"))
    if status:
        query = query.where(Candidate.status == status)
    candidates = list(db.scalars(query.limit(500)))
    if min_score is not None:
        candidates = [c for c in candidates if c.rankings and max(r.weighted_score for r in c.rankings) >= min_score]
    return candidates


@router.get("/profile/{candidate_id}", response_model=CandidateProfile)
def get_candidate(candidate_id: int, db: Session = Depends(get_db)) -> Candidate:
    candidate = db.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


@router.patch("/{candidate_id}/status", response_model=CandidateProfile)
def update_candidate_status(candidate_id: int, payload: dict, db: Session = Depends(get_db)) -> Candidate:
    candidate = db.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    status = payload.get("status")
    if status not in {"new", "shortlisted", "rejected"}:
        raise HTTPException(status_code=400, detail="Status must be new, shortlisted, or rejected")
    candidate.status = status
    db.commit()
    db.refresh(candidate)
    return candidate


@router.delete("/{candidate_id}")
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)) -> dict:
    candidate = db.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    db.delete(candidate)
    db.commit()
    return {"deleted": True}


@router.post("/{candidate_id}/match/{job_id}")
async def match_candidate(candidate_id: int, job_id: int, db: Session = Depends(get_db)) -> dict:
    candidate = db.get(Candidate, candidate_id)
    job = db.get(JobDescription, job_id)
    if not candidate or not job:
        raise HTTPException(status_code=404, detail="Candidate or job not found")
    result = score_candidate(candidate, job)
    result["summary"] = await ai_service.summarize_candidate(candidate.__dict__, result)
    ranking = Ranking(candidate_id=candidate.id, job_description_id=job.id, details=result, **{
        "match_score": result["match_score"],
        "weighted_score": result["weighted_score"],
        "suspicion_score": result["suspicion_score"],
        "hiring_recommendation": result["hiring_recommendation"],
        "confidence_score": result["confidence_score"],
    })
    db.add(ranking)
    db.commit()
    return result


@router.get("/rank/{job_id}")
def rank_candidates(job_id: int, db: Session = Depends(get_db)) -> list[dict]:
    job = db.get(JobDescription, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    rows = []
    for candidate in db.scalars(select(Candidate).limit(1000)):
        result = score_candidate(candidate, job)
        rows.append({"candidate": CandidateProfile.model_validate(candidate).model_dump(), **result})
    return sorted(rows, key=lambda item: item["weighted_score"], reverse=True)


@router.post("/{candidate_id}/questions")
async def generate_questions(candidate_id: int, db: Session = Depends(get_db)) -> dict:
    candidate = db.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    questions = await ai_service.interview_questions(candidate.__dict__)
    db.add(InterviewQuestion(candidate_id=candidate.id, questions=questions))
    db.commit()
    return questions


@router.get("/{candidate_id}/ats")
async def ats_score(candidate_id: int, db: Session = Depends(get_db)) -> dict:
    candidate = db.get(Candidate, candidate_id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return await ai_service.ats_suggestions(candidate.__dict__)


@router.get("/compare/{left_id}/{right_id}")
def compare_candidates(left_id: int, right_id: int, db: Session = Depends(get_db)) -> dict:
    left = db.get(Candidate, left_id)
    right = db.get(Candidate, right_id)
    if not left or not right:
        raise HTTPException(status_code=404, detail="Candidate not found")
    left_score = max([r.weighted_score for r in left.rankings], default=0)
    right_score = max([r.weighted_score for r in right.rankings], default=0)
    return {
        "candidate_a": CandidateProfile.model_validate(left).model_dump(),
        "candidate_b": CandidateProfile.model_validate(right).model_dump(),
        "recommendation": left.name if left_score >= right_score else right.name,
        "scores": {str(left.id): left_score, str(right.id): right_score},
    }


@router.post("/chat")
def recruiter_chat(query: dict) -> dict:
    try:
        results = get_vector_store().search(query.get("message", ""), query.get("limit", 10))
    except ImportError:
        results = get_lightweight_vector_store().search(query.get("message", ""), query.get("limit", 10))
    return {"results": results}
