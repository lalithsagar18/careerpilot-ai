import logging
from typing import List
from app.core.ai_provider import AIProvider, get_ai_provider
from app.schemas.resume import CandidateProfile
from app.schemas.job import StructuredJobData
from app.schemas.skill_gap import MissingSkill, PartialSkill
from app.schemas.learning_plan import LearningPlanCreate, LearningPlanItemCreate

logger = logging.getLogger("careerpilot.agents.learning")

LEARNING_PLAN_PROMPT = """
You are the CareerPilot AI Personalized Learning Roadmap Architect.
Design a highly actionable, structured, week-by-week technical curriculum for bridging the candidate's verified skill gaps to achieve their target job role.
Include concrete objectives, real-world project suggestions, curated learning resources, and interview practice prompts.
"""

class LearningPlanAgent:
    def __init__(self, ai_provider: AIProvider = None):
        self.ai = ai_provider or get_ai_provider()

    async def generate_plan(
        self,
        candidate: CandidateProfile,
        job: StructuredJobData,
        missing_skills: List[MissingSkill],
        partial_skills: List[PartialSkill]
    ) -> LearningPlanCreate:
        gap_names = [s.skill_name for s in missing_skills] + [s.skill_name for s in partial_skills]
        
        prompt = f"""
TARGET ROLE: {job.title} at {job.company}
CANDIDATE CURRENT SKILLS: {', '.join(candidate.technical_skills)}
IDENTIFIED SKILL GAPS: {', '.join(gap_names)}

Generate a complete LearningPlanCreate schema with realistic milestones, projects, and interview prompts:
"""
        return await self.ai.generate_structured(
            prompt=prompt,
            schema=LearningPlanCreate,
            system_instruction=LEARNING_PLAN_PROMPT
        )
