from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class ApplicationCreate(BaseModel):
    job_id: Optional[str] = None
    resume_version_id: Optional[str] = None
    company: str = Field(..., min_length=1)
    role_title: str = Field(..., min_length=1)
    status: str = "Saved"  # Saved, Preparing, Applied, Interview, Offer, Rejected, Withdrawn
    applied_date: Optional[datetime] = None
    cover_letter_text: Optional[str] = None
    notes: Optional[str] = None
    salary_offered: Optional[str] = None

class ApplicationUpdate(BaseModel):
    company: Optional[str] = None
    role_title: Optional[str] = None
    status: Optional[str] = None
    applied_date: Optional[datetime] = None
    cover_letter_text: Optional[str] = None
    notes: Optional[str] = None
    salary_offered: Optional[str] = None

class ApplicationResponse(BaseModel):
    id: str
    user_id: str
    job_id: Optional[str] = None
    resume_version_id: Optional[str] = None
    company: str
    role_title: str
    status: str
    applied_date: Optional[datetime] = None
    cover_letter_text: Optional[str] = None
    notes: Optional[str] = None
    salary_offered: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
