from typing import List, Optional
from pydantic import BaseModel, Field

class BulletRewrite(BaseModel):
    section: str
    original_bullet: str
    optimized_bullet: str
    rationale: str
    targeted_keywords: List[str] = Field(default_factory=list)
    preserves_factuality: bool = True

class ResumeOptimizationRequest(BaseModel):
    resume_id: str
    job_id: str
    custom_instructions: Optional[str] = None

class ResumeOptimizationResponse(BaseModel):
    resume_id: str
    job_id: str
    ats_score_before: float
    ats_score_projected: float
    targeted_keywords_matched: List[str]
    missing_keywords_suggested: List[str]
    bullet_rewrites: List[BulletRewrite]
    summary_rewrite: Optional[str] = None
    full_optimized_content: str
    factual_verification_notes: str
    requires_human_approval: bool = True
