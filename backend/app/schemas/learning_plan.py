from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class LearningPlanItemCreate(BaseModel):
    skill_name: str
    priority: str = "high"
    difficulty: str = "intermediate"
    objectives: List[str]
    resources: Optional[List[str]] = None
    project_suggestion: Optional[str] = None
    interview_practice_prompt: Optional[str] = None
    order_index: int = 0

class LearningPlanItemResponse(BaseModel):
    id: str
    learning_plan_id: str
    skill_name: str
    priority: str
    difficulty: str
    objectives: List[str]
    resources: Optional[List[str]] = None
    project_suggestion: Optional[str] = None
    interview_practice_prompt: Optional[str] = None
    order_index: int
    is_completed: bool

    model_config = ConfigDict(from_attributes=True)

class LearningPlanCreate(BaseModel):
    skill_gap_id: Optional[str] = None
    target_role: str
    summary: str
    estimated_weeks: int = 4
    items: List[LearningPlanItemCreate]

class LearningPlanResponse(BaseModel):
    id: str
    user_id: str
    skill_gap_id: Optional[str] = None
    target_role: str
    summary: str
    estimated_weeks: int
    completion_percentage: float
    items: List[LearningPlanItemResponse]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
