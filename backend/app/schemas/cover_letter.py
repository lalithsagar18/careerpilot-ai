from typing import List, Optional
from pydantic import BaseModel, Field

class CoverLetterRequest(BaseModel):
    resume_id: str
    job_id: str
    tone: str = "professional"  # professional, executive, energetic, technical
    target_company_notes: Optional[str] = None

class CoverLetterResponse(BaseModel):
    resume_id: str
    job_id: str
    recipient_role: Optional[str] = "Hiring Manager"
    company_name: str
    job_title: str
    salutation: str
    opening_hook: str
    body_paragraphs: List[str]
    call_to_action: str
    full_cover_letter_markdown: str
    grounded_resume_facts_used: List[str]
    requires_human_approval: bool = True
