from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.candidate import JobDescription
from app.schemas.job import JobDescriptionCreate, JobDescriptionRead
from app.services.job_analyzer import analyze_job_description

router = APIRouter()


@router.post("", response_model=JobDescriptionRead)
def create_job(payload: JobDescriptionCreate, db: Session = Depends(get_db)) -> JobDescription:
    analyzed = analyze_job_description(payload.description)
    job = JobDescription(title=payload.title, description=payload.description, **analyzed)
    db.add(job)
    db.commit()
    db.refresh(job)
    return job
