from typing import List, Optional
from pydantic import BaseModel, Field

class EvaluationResult(BaseModel):
    factual_consistency_score: float = Field(..., ge=0.0, le=1.0)
    groundedness_score: float = Field(..., ge=0.0, le=1.0)
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    quality_score: float = Field(..., ge=0.0, le=1.0)
    passes_threshold: bool
    detected_hallucinations: List[str] = Field(default_factory=list)
    critique_notes: str
    suggested_revisions: List[str] = Field(default_factory=list)

class HumanApprovalRequest(BaseModel):
    artifact_type: str  # resume_version, cover_letter, learning_plan
    artifact_id: str
    decision: str  # approve, reject, edit
    edited_content: Optional[str] = None
    feedback: Optional[str] = None
