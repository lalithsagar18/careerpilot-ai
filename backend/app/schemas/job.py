from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class JobCreate(BaseModel):
    title: str = Field(..., min_length=2)
    company: str = Field(..., min_length=2)
    location: Optional[str] = "Remote"
    employment_type: Optional[str] = "Full-time"
    seniority: Optional[str] = "Mid-Senior"
    source_url: Optional[str] = None
    raw_description: str = Field(..., min_length=20)

class JobRequirementItem(BaseModel):
    category: str  # required_skill, preferred_skill, education, experience, technology
    requirement_text: str
    weight: float = 1.0
    normalized_name: Optional[str] = None

class StructuredJobData(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    employment_type: Optional[str] = None
    seniority: Optional[str] = None
    summary: Optional[str] = None
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    required_technologies: List[str] = Field(default_factory=list)
    required_years_experience: Optional[float] = None
    required_education: Optional[str] = None
    responsibilities: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)

class JobResponse(BaseModel):
    id: str
    user_id: str
    title: str
    company: str
    location: Optional[str] = None
    employment_type: Optional[str] = None
    seniority: Optional[str] = None
    source_url: Optional[str] = None
    raw_description: str
    parsed_data: Optional[StructuredJobData] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
