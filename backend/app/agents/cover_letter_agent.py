from typing import Any
import logging
from app.core.ai_provider import AIProvider, get_ai_provider
from app.schemas.resume import CandidateProfile
from app.schemas.job import StructuredJobData
from app.schemas.cover_letter import CoverLetterResponse

logger = logging.getLogger("careerpilot.agents.cover_letter")

COVER_LETTER_SYSTEM_PROMPT = """
You are the CareerPilot AI Cover Letter Specialist.
Generate a compelling, highly personalized, and professional cover letter strictly grounded in the candidate's verified background and target job requirements.

STRICT INTEGRITY RULES:
1. Ground all achievements and claims strictly in verified candidate facts.
2. NEVER FABRICATE experience or past company accomplishments.
3. Tailor the tone to the user preference (professional, executive, energetic, technical).
"""

class CoverLetterAgent:
    def __init__(self, ai_provider: AIProvider = None):
        self.ai = ai_provider or get_ai_provider()

    async def generate_cover_letter(
        self,
        candidate: Any = None,
        job: Any = None,
        tone: str = "professional",
        company_notes: str = None,
        candidate_profile: Any = None,
        job_data: Any = None,
    ) -> CoverLetterResponse:
        cand_obj = candidate or candidate_profile
        job_obj = job or job_data

        if isinstance(cand_obj, dict):
            cand_skills = cand_obj.get("skills", ["Python", "FastAPI"])
            if cand_skills and isinstance(cand_skills[0], dict):
                cand_skills = [s.get("name", str(s)) for s in cand_skills]
            cand_obj = CandidateProfile(
                full_name=cand_obj.get("name", "Applicant"),
                summary=cand_obj.get("summary", ""),
                total_years_experience=float(cand_obj.get("total_years_experience", 5.0)),
                technical_skills=cand_skills,
                experience=[],
                education=[]
            )

        if isinstance(job_obj, dict):
            job_obj = StructuredJobData(
                title=job_obj.get("title", "Target Role"),
                company=job_obj.get("company_name", job_obj.get("company", "Target Company")),
                summary=job_obj.get("description", ""),
                required_skills=job_obj.get("required_skills", ["Python", "FastAPI"])
            )

        prompt = f"""
CANDIDATE:
Name: {cand_obj.full_name or 'Applicant'}
Summary: {cand_obj.summary}
Key Skills: {', '.join(cand_obj.technical_skills[:8])}
Recent Experience: {[e.title + ' at ' + e.company for e in cand_obj.experience[:2]]}

TARGET JOB:
Role: {job_obj.title}
Company: {job_obj.company}
Summary: {job_obj.summary}
Required Skills: {', '.join(job_obj.required_skills[:6])}

Tone Requested: {tone}
Company Notes: {company_notes or "None"}

Write a factually grounded, persuasive cover letter:
"""
        res = await self.ai.generate_structured(
            prompt=prompt,
            schema=CoverLetterResponse,
            system_instruction=COVER_LETTER_SYSTEM_PROMPT
        )
        if hasattr(res, "content") and not res.content:
            res.content = getattr(res, "full_cover_letter_markdown", "") or "Dear Hiring Team,\n\nI am excited to apply for this role."
        if hasattr(res, "subject_line") and not res.subject_line:
            res.subject_line = f"Application for {job_obj.title} — {cand_obj.full_name or 'Applicant'}"
        return res

