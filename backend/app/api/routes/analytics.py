from collections import Counter

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.candidate import Candidate, Ranking

router = APIRouter()


@router.get("/dashboard")
def dashboard(db: Session = Depends(get_db)) -> dict:
    candidates = list(db.scalars(select(Candidate)))
    rankings = list(db.scalars(select(Ranking)))
    skills = Counter(skill for candidate in candidates for skill in (candidate.skills or []))
    avg_score = sum(r.weighted_score for r in rankings) / max(len(rankings), 1)
    return {
        "total_candidates": len(candidates),
        "average_match_score": round(avg_score, 2),
        "top_skills": skills.most_common(10),
        "candidates_by_experience_level": {
            "fresher": len([c for c in candidates if c.experience_years < 1]),
            "mid": len([c for c in candidates if 1 <= c.experience_years < 5]),
            "senior": len([c for c in candidates if c.experience_years >= 5]),
        },
        "shortlisted_candidates": len([c for c in candidates if c.status == "shortlisted"]),
        "rejected_candidates": len([c for c in candidates if c.status == "rejected"]),
    }
