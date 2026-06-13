from app.models.candidate import Candidate, JobDescription


WEIGHTS = {
    "skills": 0.40,
    "experience": 0.25,
    "projects": 0.15,
    "education": 0.10,
    "certifications": 0.10,
}


def score_candidate(candidate: Candidate, job: JobDescription) -> dict:
    required = set(job.required_skills or [])
    preferred = set(job.preferred_skills or [])
    target_skills = required | preferred
    candidate_skills = set(candidate.skills or [])
    matched = sorted(candidate_skills & target_skills)
    missing = sorted(required - candidate_skills)
    skill_score = len(matched) / max(len(target_skills), 1) * 100
    min_years = float((job.experience_requirements or {}).get("minimum_years", 0))
    experience_score = min(candidate.experience_years / max(min_years, 1), 1) * 100
    project_score = min(len(candidate.projects or []) / 3, 1) * 100
    education_score = 100 if candidate.education else 45
    certification_score = min(len(candidate.certifications or []) / 2, 1) * 100
    weighted = (
        skill_score * WEIGHTS["skills"]
        + experience_score * WEIGHTS["experience"]
        + project_score * WEIGHTS["projects"]
        + education_score * WEIGHTS["education"]
        + certification_score * WEIGHTS["certifications"]
    )
    suspicion = suspicion_score(candidate)
    recommendation, confidence = recommendation_for(weighted, suspicion)
    return {
        "match_score": round(skill_score, 2),
        "weighted_score": round(weighted, 2),
        "component_scores": {
            "skills": round(skill_score, 2),
            "experience": round(experience_score, 2),
            "projects": round(project_score, 2),
            "education": round(education_score, 2),
            "certifications": round(certification_score, 2),
        },
        "weights": {key: int(value * 100) for key, value in WEIGHTS.items()},
        "matching_skills": matched,
        "missing_skills": missing,
        "strengths": strengths(candidate, matched),
        "suspicion_score": suspicion,
        "hiring_recommendation": recommendation,
        "confidence_score": confidence,
    }


def strengths(candidate: Candidate, matched: list[str]) -> list[str]:
    items = []
    if matched:
        items.append(f"Relevant skills: {', '.join(matched[:8])}")
    if candidate.projects:
        items.append(f"{len(candidate.projects)} project entries found")
    if candidate.experience_years:
        items.append(f"{candidate.experience_years:g} years of experience indicated")
    return items or ["Profile has parseable structured resume data"]


def suspicion_score(candidate: Candidate) -> int:
    score = 0
    if candidate.experience_years >= 5 and len(candidate.experience or []) == 0:
        score += 35
    if len(candidate.skills or []) > 18 and len(candidate.projects or []) < 2:
        score += 25
    if candidate.experience_years >= 3 and len(candidate.projects or []) == 0:
        score += 20
    if any("react" in skill.lower() for skill in candidate.skills or []) and candidate.experience_years >= 8:
        score += 10
    return min(score, 100)


def recommendation_for(weighted_score: float, suspicion: int) -> tuple[str, int]:
    adjusted = max(0, weighted_score - suspicion * 0.25)
    if adjusted >= 85:
        return "Strong Hire", min(98, round(adjusted))
    if adjusted >= 70:
        return "Hire", round(adjusted)
    if adjusted >= 50:
        return "Consider", round(adjusted)
    return "Reject", max(15, round(adjusted))
