import csv
from io import StringIO

from fastapi import APIRouter, Depends, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.candidate import Candidate

router = APIRouter()


@router.get("/candidates.csv")
def candidate_csv(db: Session = Depends(get_db)) -> Response:
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Name", "Email", "Phone", "Skills", "Experience Years", "Status"])
    for candidate in db.scalars(select(Candidate)):
        writer.writerow([
            candidate.name,
            candidate.email,
            candidate.phone,
            ", ".join(candidate.skills or []),
            candidate.experience_years,
            candidate.status,
        ])
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=talentiq-candidates.csv"},
    )
