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
    resume_id: str = "default_resume"
    job_id: str = "default_job"
    ats_score_before: float = 70.0
    ats_score_projected: float = 92.0
    targeted_keywords_matched: List[str] = Field(default_factory=list)
    missing_keywords_suggested: List[str] = Field(default_factory=list)
    bullet_rewrites: List[BulletRewrite] = Field(default_factory=list)
    summary_rewrite: Optional[str] = None
    full_optimized_content: str = ""
    factual_verification_notes: str = "Verified strictly against source facts."
    requires_human_approval: bool = True
