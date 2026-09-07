from typing import List, Optional
from pydantic import BaseModel, Field

class CoverLetterRequest(BaseModel):
    resume_id: str
    job_id: str
    tone: str = "professional"  # professional, executive, energetic, technical
    target_company_notes: Optional[str] = None

class CoverLetterResponse(BaseModel):
    resume_id: str = "default_resume"
    job_id: str = "default_job"
    recipient_role: Optional[str] = "Hiring Manager"
    company_name: str = "TechCorp"
    job_title: str = "Senior Engineer"
    salutation: str = "Dear Hiring Team,"
    opening_hook: str = "I am excited to apply for this role."
    body_paragraphs: List[str] = Field(default_factory=list)
    call_to_action: str = "I welcome the opportunity to discuss my qualifications."
    full_cover_letter_markdown: str = ""
    grounded_resume_facts_used: List[str] = Field(default_factory=list)
    requires_human_approval: bool = True
    subject_line: Optional[str] = None
    content: Optional[str] = None
