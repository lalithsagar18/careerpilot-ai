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
        candidate: CandidateProfile,
        job: StructuredJobData,
        tone: str = "professional",
        company_notes: str = None
    ) -> CoverLetterResponse:
        prompt = f"""
CANDIDATE:
Name: {candidate.full_name or 'Applicant'}
Summary: {candidate.summary}
Key Skills: {', '.join(candidate.technical_skills[:8])}
Recent Experience: {[e.title + ' at ' + e.company for e in candidate.experience[:2]]}

TARGET JOB:
Role: {job.title}
Company: {job.company}
Summary: {job.summary}
Required Skills: {', '.join(job.required_skills[:6])}

Tone Requested: {tone}
Company Notes: {company_notes or "None"}

Write a factually grounded, persuasive cover letter:
"""
        return await self.ai.generate_structured(
            prompt=prompt,
            schema=CoverLetterResponse,
            system_instruction=COVER_LETTER_SYSTEM_PROMPT
        )
