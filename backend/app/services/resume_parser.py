import re
from dataclasses import dataclass


SKILL_CATALOG = {
    "python", "java", "javascript", "typescript", "react", "node.js", "fastapi",
    "django", "flask", "sql", "postgresql", "mysql", "mongodb", "power bi",
    "tableau", "machine learning", "deep learning", "nlp", "pandas", "numpy",
    "scikit-learn", "tensorflow", "pytorch", "aws", "azure", "gcp", "docker",
    "kubernetes", "git", "linux", "langchain", "chromadb", "excel",
}


@dataclass
class ParsedResume:
    name: str | None
    email: str | None
    phone: str | None
    skills: list[str]
    education: list[dict]
    certifications: list[str]
    experience: list[dict]
    projects: list[dict]
    internships: list[dict]
    linkedin_url: str | None
    github_url: str | None
    experience_years: float

    def asdict(self) -> dict:
        return self.__dict__


def parse_resume_text(text: str) -> ParsedResume:
    normalized = _normalize(text)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    email = _first_match(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
    phone = _first_match(r"(?:\+?\d[\s-]?){10,15}", text)
    linkedin = _first_match(r"https?://(?:www\.)?linkedin\.com/[^\s)]+", text)
    github = _first_match(r"https?://(?:www\.)?github\.com/[^\s)]+", text)
    skills = sorted(skill for skill in SKILL_CATALOG if skill in normalized)
    name = _infer_name(lines, email)
    return ParsedResume(
        name=name,
        email=email,
        phone=phone,
        skills=skills,
        education=_extract_sections(lines, ("education", "academics")),
        certifications=_extract_certifications(lines),
        experience=_extract_sections(lines, ("experience", "employment", "work history")),
        projects=_extract_sections(lines, ("projects", "academic projects")),
        internships=_extract_sections(lines, ("internship", "internships")),
        linkedin_url=linkedin,
        github_url=github,
        experience_years=_extract_years(text),
    )


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower())


def _first_match(pattern: str, text: str) -> str | None:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    return match.group(0).strip() if match else None


def _infer_name(lines: list[str], email: str | None) -> str | None:
    for line in lines[:8]:
        if "@" in line or "http" in line.lower() or len(line.split()) > 5:
            continue
        if re.search(r"\d", line):
            continue
        return line.title()
    return email.split("@")[0].replace(".", " ").title() if email else None


def _extract_sections(lines: list[str], headings: tuple[str, ...]) -> list[dict]:
    results: list[dict] = []
    active = False
    for line in lines:
        lower = line.lower()
        if any(heading in lower for heading in headings):
            active = True
            continue
        if active and re.match(r"^[A-Z][A-Za-z ]{2,25}:?$", line) and len(results) > 0:
            break
        if active and len(line) > 12:
            results.append({"description": line})
        if len(results) >= 8:
            break
    return results


def _extract_certifications(lines: list[str]) -> list[str]:
    return [
        line for line in lines
        if any(word in line.lower() for word in ("certified", "certification", "certificate"))
    ][:10]


def _extract_years(text: str) -> float:
    normalized = _normalize(text)
    explicit = re.findall(r"(\d+(?:\.\d+)?)\+?\s+years?\s+(?:of\s+)?(?:professional\s+)?experience", normalized)
    if explicit:
        return max(float(year) for year in explicit)

    experience_text = _experience_only_text(text)
    if not experience_text:
        return 0

    ranges = re.findall(r"(20\d{2}|19\d{2})\s*[-–]\s*(20\d{2}|present|current)", _normalize(experience_text))
    total = 0
    for start, end in ranges:
        end_year = 2026 if end in {"present", "current"} else int(end)
        total += max(0, end_year - int(start))
    return float(min(total, 40))


def _experience_only_text(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    capture_headings = ("experience", "employment", "work history", "internship", "internships")
    stop_headings = (
        "education", "academics", "skills", "projects", "certifications",
        "certificate", "achievements", "summary", "profile",
    )
    captured: list[str] = []
    active = False
    for line in lines:
        lower = line.lower().strip(":")
        if any(heading == lower or heading in lower for heading in capture_headings):
            active = True
            continue
        if active and any(heading == lower or heading in lower for heading in stop_headings):
            break
        if active:
            captured.append(line)
    return "\n".join(captured)
