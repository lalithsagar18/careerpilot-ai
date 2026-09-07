from typing import List, Any, Optional
import logging
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
        candidate: Any = None,
        job: Any = None,
        missing_skills: List[Any] = None,
        partial_skills: List[Any] = None,
        target_role: str = None,
        skill_gaps: list = None
    ) -> Any:
        # Handle Streamlit or simplified positional signature (target_role, skill_gaps)
        if isinstance(candidate, str):
            role_str = candidate
            gaps_in = job if isinstance(job, list) else (skill_gaps or [])
            gap_names = []
            for g in gaps_in:
                if isinstance(g, dict):
                    gap_names.append(g.get("skill_name", str(g)))
                else:
                    gap_names.append(str(g))
            
            prompt = f"""
TARGET ROLE: {role_str}
IDENTIFIED SKILL GAPS: {', '.join(gap_names) if gap_names else 'General Mastery'}

Generate a structured 30-60-90 day learning curriculum:
"""
            res = await self.ai.generate_structured(
                prompt=prompt,
                schema=LearningPlanCreate,
                system_instruction=LEARNING_PLAN_PROMPT
            )
            # Return dict format if called with simplified strings
            return {
                "title": f"Skill Mastery Plan: {role_str}",
                "description": res.summary,
                "items": [
                    {
                        "day_milestone": (it.order_index or idx + 1) * 30,
                        "title": f"Phase {idx+1}: {it.skill_name}",
                        "description": "; ".join(it.objectives),
                        "resource_links": it.resources or ["Official Documentation"]
                    }
                    for idx, it in enumerate(res.items)
                ]
            }

        # Handle structured CandidateProfile and StructuredJobData
        cand_skills = candidate.technical_skills if candidate and hasattr(candidate, 'technical_skills') else ["Python"]
        job_title = job.title if job and hasattr(job, 'title') else "Target Role"
        job_comp = job.company if job and hasattr(job, 'company') else "Target Company"

        gap_names = []
        if missing_skills:
            gap_names += [s.skill_name if hasattr(s, 'skill_name') else str(s) for s in missing_skills]
        if partial_skills:
            gap_names += [s.skill_name if hasattr(s, 'skill_name') else str(s) for s in partial_skills]

        prompt = f"""
TARGET ROLE: {job_title} at {job_comp}
CANDIDATE CURRENT SKILLS: {', '.join(cand_skills)}
IDENTIFIED SKILL GAPS: {', '.join(gap_names) if gap_names else 'Core Competencies'}

Generate a complete LearningPlanCreate schema with realistic milestones, projects, and interview prompts:
"""
        return await self.ai.generate_structured(
            prompt=prompt,
            schema=LearningPlanCreate,
            system_instruction=LEARNING_PLAN_PROMPT
        )

