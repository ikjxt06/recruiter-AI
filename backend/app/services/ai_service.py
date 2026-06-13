import google.generativeai as genai

from app.core.config import settings


class AIService:
    def __init__(self) -> None:
        self.enabled = bool(settings.gemini_api_key)
        if self.enabled:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel(settings.gemini_model)
        else:
            self.model = None

    async def summarize_candidate(self, profile: dict, match: dict) -> str:
        if not self.enabled:
            skills = ", ".join((profile.get("skills") or [])[:6])
            return f"Candidate shows alignment through {skills or 'documented resume evidence'} with a {match['weighted_score']} weighted score."
        prompt = f"Write a concise recruiter summary for this candidate.\nProfile: {profile}\nMatch: {match}"
        response = self.model.generate_content(prompt)
        return response.text.strip()

    async def interview_questions(self, profile: dict) -> dict:
        skills = profile.get("skills") or []
        technical = [f"Explain a production use case for {skill}." for skill in skills[:5]]
        return {
            "technical": technical or ["Explain a recent technical problem you solved."],
            "project_based": ["Walk through your most relevant project architecture."],
            "behavioral": ["Tell me about a time you handled ambiguous requirements."],
        }

    async def ats_suggestions(self, profile: dict) -> dict:
        score = 70
        suggestions = []
        if not profile.get("projects"):
            suggestions.append("Add project outcomes with measurable impact.")
        if len(profile.get("skills") or []) < 8:
            suggestions.append("Improve keyword coverage for target roles.")
        if not profile.get("certifications"):
            suggestions.append("Add relevant certifications or coursework when available.")
        score += min(20, len(profile.get("skills") or []))
        return {"ats_score": min(score, 100), "suggestions": suggestions}


ai_service = AIService()
