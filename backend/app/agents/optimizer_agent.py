import logging
from typing import List, Any
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
        candidate: Any = None, 
        job: Any = None,
        custom_instructions: str = None,
        candidate_profile: Any = None,
        job_requirements: Any = None,
        target_keywords: List[str] = None
    ) -> ResumeOptimizationResponse:
        cand_obj = candidate or candidate_profile
        job_obj = job or job_requirements

        # Handle dict inputs
        if isinstance(cand_obj, dict):
            cand_skills = cand_obj.get("skills", ["Python", "FastAPI", "PostgreSQL"])
            if cand_skills and isinstance(cand_skills[0], dict):
                cand_skills = [s.get("name", str(s)) for s in cand_skills]
            cand_obj = CandidateProfile(
                full_name=cand_obj.get("name", "Candidate"),
                summary=cand_obj.get("summary", ""),
                total_years_experience=float(cand_obj.get("total_years_experience", 5.0)),
                technical_skills=cand_skills,
                experience=[],
                education=[]
            )

        if isinstance(job_obj, dict):
            job_skills = job_obj.get("required_skills", target_keywords or ["Python", "FastAPI"])
            job_obj = StructuredJobData(
                title=job_obj.get("title", "Target Role"),
                company=job_obj.get("company_name", job_obj.get("company", "Target Company")),
                required_skills=job_skills,
                preferred_skills=job_obj.get("preferred_skills", []),
                keywords=target_keywords or job_skills
            )

        prompt = f"""
TARGET JOB:
Title: {job_obj.title} at {job_obj.company}
Required Skills: {', '.join(job_obj.required_skills)}
Keywords: {', '.join(job_obj.keywords)}

VERIFIED CANDIDATE PROFILE:
Summary: {cand_obj.summary}
Technical Skills: {', '.join(cand_obj.technical_skills)}
Experience: {[e.model_dump() for e in cand_obj.experience]}
Projects: {[p.model_dump() for p in cand_obj.projects]}

Custom User Instructions: {custom_instructions or "None"}

Generate an optimized version with bullet rewrites, ATS improvements, and keyword matching:
"""
        return await self.ai.generate_structured(
            prompt=prompt,
            schema=ResumeOptimizationResponse,
            system_instruction=OPTIMIZER_SYSTEM_PROMPT
        )

# Export alias for compatibility
ResumeOptimizerAgent = ResumeOptimizationAgent

