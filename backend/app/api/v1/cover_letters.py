import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User
from app.models.resume import Resume
from app.models.job import Job
from app.schemas.cover_letter import CoverLetterRequest, CoverLetterResponse
from app.schemas.resume import CandidateProfile
from app.schemas.job import StructuredJobData
from app.api.deps import get_current_user
from app.agents.cover_letter_agent import CoverLetterAgent

router = APIRouter(prefix="/cover-letters", tags=["Cover Letters"])

@router.post("", response_model=CoverLetterResponse)
async def generate_cover_letter(
    payload: CoverLetterRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    res_stmt = select(Resume).where(Resume.id == payload.resume_id, Resume.user_id == current_user.id)
    resume = (await db.execute(res_stmt)).scalars().first()
    if not resume or not resume.candidate_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")

    job_stmt = select(Job).where(Job.id == payload.job_id, Job.user_id == current_user.id)
    job = (await db.execute(job_stmt)).scalars().first()
    if not job or not job.parsed_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found.")

    cand = CandidateProfile.model_validate(json.loads(resume.candidate_profile))
    job_data = StructuredJobData.model_validate(json.loads(job.parsed_data))

    agent = CoverLetterAgent()
    return await agent.generate_cover_letter(
        candidate=cand,
        job=job_data,
        tone=payload.tone,
        company_notes=payload.target_company_notes
    )
