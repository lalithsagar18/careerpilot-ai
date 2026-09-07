from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class ExperienceItem(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    is_current: bool = False
    highlights: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)

class EducationItem(BaseModel):
    degree: str
    institution: str
    field_of_study: Optional[str] = None
    graduation_year: Optional[str] = None
    gpa: Optional[str] = None

class ProjectItem(BaseModel):
    name: str
    description: str
    technologies: List[str] = Field(default_factory=list)
    link: Optional[str] = None
    metrics: List[str] = Field(default_factory=list)

class CertificationItem(BaseModel):
    name: str
    issuer: str
    issue_date: Optional[str] = None
    expiration_date: Optional[str] = None
    credential_id: Optional[str] = None

class CandidateProfile(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    total_years_experience: Optional[float] = None
    technical_skills: List[str] = Field(default_factory=list)
    soft_skills: List[str] = Field(default_factory=list)
    tools_and_platforms: List[str] = Field(default_factory=list)
    experience: List[ExperienceItem] = Field(default_factory=list)
    education: List[EducationItem] = Field(default_factory=list)
    projects: List[ProjectItem] = Field(default_factory=list)
    certifications: List[CertificationItem] = Field(default_factory=list)
    achievements: List[str] = Field(default_factory=list)

class ResumeQualityAssessment(BaseModel):
    overall_health_score: float = Field(..., ge=0, le=100)
    completeness_score: float = Field(..., ge=0, le=100)
    action_verb_score: float = Field(..., ge=0, le=100)
    metrics_quantification_score: float = Field(..., ge=0, le=100)
    formatting_score: float = Field(..., ge=0, le=100)
    missing_sections: List[str] = Field(default_factory=list)
    weak_descriptions: List[str] = Field(default_factory=list)
    actionable_recommendations: List[str] = Field(default_factory=list)

class ResumeResponse(BaseModel):
    id: str
    user_id: str
    title: str
    file_name: str
    file_type: str
    file_size_bytes: int
    health_score: Optional[float] = None
    candidate_profile: Optional[CandidateProfile] = None
    health_assessment: Optional[ResumeQualityAssessment] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ResumeVersionResponse(BaseModel):
    id: str
    resume_id: str
    version_number: int
    target_job_id: Optional[str] = None
    ats_score: Optional[float] = None
    change_summary: Optional[str] = None
    is_approved: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
