import re

from app.services.resume_parser import SKILL_CATALOG


def analyze_job_description(description: str) -> dict:
    normalized = re.sub(r"\s+", " ", description.lower())
    found = sorted(skill for skill in SKILL_CATALOG if skill in normalized)
    preferred_markers = ("preferred", "nice to have", "bonus", "plus")
    preferred = [skill for skill in found if any(marker in normalized for marker in preferred_markers)]
    required = [skill for skill in found if skill not in preferred] or found
    years = re.findall(r"(\d+)\+?\s+years?", normalized)
    return {
        "required_skills": required,
        "preferred_skills": preferred,
        "experience_requirements": {
            "minimum_years": int(max(years, key=int)) if years else 0,
            "raw": ", ".join(years),
        },
    }
