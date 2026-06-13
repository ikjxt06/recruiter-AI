from pydantic import BaseModel, EmailStr


class CandidateProfile(BaseModel):
    id: int
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = None
    linkedin_url: str | None = None
    github_url: str | None = None
    skills: list[str] = []
    education: list[dict] = []
    certifications: list[str] = []
    experience: list[dict] = []
    projects: list[dict] = []
    internships: list[dict] = []
    experience_years: float = 0
    status: str = "new"

    class Config:
        from_attributes = True


class CandidateMatch(BaseModel):
    candidate_id: int
    match_score: float
    matching_skills: list[str]
    missing_skills: list[str]
    strengths: list[str]
    suspicion_score: int
    hiring_recommendation: str
    confidence_score: int
    summary: str
