from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class MatchedSkill(BaseModel):
    skill_name: str
    category: str
    candidate_evidence: Optional[str] = None
    job_requirement: Optional[str] = None
    confidence: float = 1.0

class MissingSkill(BaseModel):
    skill_name: str
    category: str
    importance: str = "critical"  # critical, high, medium, low
    job_context: Optional[str] = None

class PartialSkill(BaseModel):
    skill_name: str
    gap_description: str
    current_level: str
    target_level: str

class ScoreBreakdown(BaseModel):
    overall_score: float = Field(..., ge=0, le=100)
    required_skill_score: float = Field(..., ge=0, le=100)
    preferred_skill_score: float = Field(..., ge=0, le=100)
    experience_score: float = Field(..., ge=0, le=100)
    technology_score: float = Field(..., ge=0, le=100)
    education_score: float = Field(..., ge=0, le=100)
    weights_applied: Dict[str, float]

class SkillGapCalculateRequest(BaseModel):
    resume_id: str
    job_id: str

class SkillGapResponse(BaseModel):
    id: str
    user_id: str
    resume_id: str
    job_id: str
    score_breakdown: ScoreBreakdown
    matching_skills: List[MatchedSkill]
    missing_skills: List[MissingSkill]
    partial_skills: List[PartialSkill]
    explanation: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
