from typing import List, Optional, Dict
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class InterviewStartRequest(BaseModel):
    job_id: Optional[str] = None
    target_role: str = "Software Engineer"
    interview_type: str = "Technical"  # Technical, Behavioral, System Design, Data Science, Python, SQL, ML
    total_questions: int = Field(default=5, ge=1, le=10)

class InterviewQuestionResponse(BaseModel):
    id: str
    interview_id: str
    question_text: str
    category: str
    difficulty: str
    order_index: int
    is_follow_up: bool

    model_config = ConfigDict(from_attributes=True)

class InterviewSubmitAnswerRequest(BaseModel):
    question_id: str
    user_answer_text: str = Field(..., min_length=5)

class InterviewAnswerFeedback(BaseModel):
    score: float = Field(..., ge=0, le=100)
    technical_accuracy_score: float = 85.0
    relevance_score: float = 85.0
    depth_score: float = 85.0
    communication_score: float = 85.0
    feedback: str = ""
    strengths: List[str] = Field(default_factory=list)
    missed_points: List[str] = Field(default_factory=list)
    improvements: List[str] = Field(default_factory=list)
    suggested_ideal_answer: Optional[str] = None
    model_answer: Optional[str] = None

class InterviewReport(BaseModel):
    id: str
    user_id: str
    target_role: str
    interview_type: str
    status: str
    overall_score: Optional[float] = None
    category_scores: Optional[Dict[str, float]] = None
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    improvement_plan: Optional[str] = None
    suggested_study_topics: List[str] = Field(default_factory=list)
    total_questions: int
    questions_answered: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
