import logging
from typing import List
from app.core.ai_provider import AIProvider, get_ai_provider
from app.schemas.resume import CandidateProfile
from app.schemas.job import StructuredJobData
from app.schemas.optimizer import ResumeOptimizationResponse, BulletRewrite

logger = logging.getLogger("careerpilot.agents.optimizer")

OPTIMIZER_SYSTEM_PROMPT = """
You are the CareerPilot AI Resume Optimization Agent.
Your role is to enhance resume bullets and align keyword descriptions with target job requirements.

STRICT NON-NEGOTIABLE INTEGRITY RULES:
1. NEVER INVENT EXPERIENCES, COMPANIES, METRICS, TECHNOLOGIES, OR CREDENTIALS.
2. Only reframe and polish real facts already present in the candidate profile.
3. Quantify impact using the candidate's verified figures (never hallucinate random 10x or percentages).
4. Highlight relevant keywords naturally to optimize ATS pass rates.
5. Provide a clear rationale and verification note confirming no facts were fabricated.
"""

class ResumeOptimizationAgent:
    def __init__(self, ai_provider: AIProvider = None):
        self.ai = ai_provider or get_ai_provider()

    async def optimize_resume(
        self, 
        candidate: CandidateProfile, 
        job: StructuredJobData,
        custom_instructions: str = None
    ) -> ResumeOptimizationResponse:
        prompt = f"""
TARGET JOB:
Title: {job.title} at {job.company}
Required Skills: {', '.join(job.required_skills)}
Keywords: {', '.join(job.keywords)}

VERIFIED CANDIDATE PROFILE:
Summary: {candidate.summary}
Technical Skills: {', '.join(candidate.technical_skills)}
Experience: {[e.model_dump() for e in candidate.experience]}
Projects: {[p.model_dump() for p in candidate.projects]}

Custom User Instructions: {custom_instructions or "None"}

Generate an optimized version with bullet rewrites, ATS improvements, and keyword matching:
"""
        return await self.ai.generate_structured(
            prompt=prompt,
            schema=ResumeOptimizationResponse,
            system_instruction=OPTIMIZER_SYSTEM_PROMPT
        )
