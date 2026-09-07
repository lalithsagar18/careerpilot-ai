import logging
from typing import Tuple
from app.core.ai_provider import AIProvider, get_ai_provider
from app.schemas.resume import CandidateProfile, ResumeQualityAssessment

logger = logging.getLogger("careerpilot.agents.resume")

RESUME_PARSER_SYSTEM_PROMPT = """
You are the CareerPilot AI Resume Intelligence Agent.
Your duty is to extract verified facts from the candidate's uploaded resume and structure them into a CandidateProfile schema.

CRITICAL NON-NEGOTIABLE SAFETY & INTEGRITY RULES:
1. NEVER FABRICATE OR HALLUCINATE ANY INFORMATION.
2. Never invent companies, dates, degrees, projects, skills, certifications, or metrics.
3. If information is not explicitly mentioned or clearly implied in the text, leave it empty/null.
4. Normalize skills into clear, industry-standard terms.
5. Extract all quantified metrics exactly as stated by the candidate.
"""

RESUME_ASSESSMENT_SYSTEM_PROMPT = """
You are an expert ATS (Applicant Tracking System) and Technical Recruiter.
Analyze the extracted candidate profile and resume text for structure, completeness, action verbs, quantified metrics, and formatting strength.
Score each dimension from 0 to 100 and provide constructive recommendations.
"""

class ResumeIntelligenceAgent:
    def __init__(self, ai_provider: AIProvider = None):
        self.ai = ai_provider or get_ai_provider()

    async def parse_resume(self, raw_resume_text: str) -> CandidateProfile:
        prompt = f"""
Please parse the following raw resume text into a structured CandidateProfile:

--- BEGIN RESUME ---
{raw_resume_text}
--- END RESUME ---
"""
        profile = await self.ai.generate_structured(
            prompt=prompt,
            schema=CandidateProfile,
            system_instruction=RESUME_PARSER_SYSTEM_PROMPT
        )
        return profile

    async def assess_resume_quality(
        self, 
        raw_resume_text: str, 
        profile: CandidateProfile
    ) -> ResumeQualityAssessment:
        prompt = f"""
Candidate Summary: {profile.summary}
Technical Skills: {', '.join(profile.technical_skills)}
Experience Count: {len(profile.experience)}
Education: {', '.join([e.degree for e in profile.education])}

Evaluate the resume's quality, completeness, action verb usage, and quantified achievements.
"""
        assessment = await self.ai.generate_structured(
            prompt=prompt,
            schema=ResumeQualityAssessment,
            system_instruction=RESUME_ASSESSMENT_SYSTEM_PROMPT
        )
        return assessment
