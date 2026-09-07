import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User
from app.models.job import Job, JobRequirement
from app.schemas.job import JobCreate, JobResponse, StructuredJobData
from app.api.deps import get_current_user
from app.agents.job_agent import JobResearchAgent

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_and_analyze_job(
    job_in: JobCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    agent = JobResearchAgent()
    
    # If source URL provided and description empty or requested URL ingestion
    if job_in.source_url and len(job_in.raw_description) < 50:
        structured_data = await agent.analyze_from_url(job_in.source_url)
    else:
        structured_data = await agent.analyze_job(job_in.raw_description)

    job = Job(
        user_id=current_user.id,
        title=job_in.title or structured_data.title,
        company=job_in.company or structured_data.company,
        location=job_in.location or structured_data.location,
        employment_type=job_in.employment_type or structured_data.employment_type,
        seniority=job_in.seniority or structured_data.seniority,
        source_url=job_in.source_url,
        raw_description=job_in.raw_description,
        parsed_data=json.dumps(structured_data.model_dump())
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)

    # Persist job requirement items for indexing
    for req in structured_data.required_skills:
        db.add(JobRequirement(job_id=job.id, category="required_skill", requirement_text=req))
    for pref in structured_data.preferred_skills:
        db.add(JobRequirement(job_id=job.id, category="preferred_skill", requirement_text=pref))
    await db.commit()

    return JobResponse(
        id=job.id,
        user_id=job.user_id,
        title=job.title,
        company=job.company,
        location=job.location,
        employment_type=job.employment_type,
        seniority=job.seniority,
        source_url=job.source_url,
        raw_description=job.raw_description,
        parsed_data=structured_data,
        created_at=job.created_at
    )

@router.get("", response_model=List[JobResponse])
async def list_jobs(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Job).where(Job.user_id == current_user.id).order_by(Job.created_at.desc())
    result = await db.execute(stmt)
    jobs = result.scalars().all()

    res = []
    for j in jobs:
        data = StructuredJobData.model_validate(json.loads(j.parsed_data)) if j.parsed_data else None
        res.append(JobResponse(
            id=j.id,
            user_id=j.user_id,
            title=j.title,
            company=j.company,
            location=j.location,
            employment_type=j.employment_type,
            seniority=j.seniority,
            source_url=j.source_url,
            raw_description=j.raw_description,
            parsed_data=data,
            created_at=j.created_at
        ))
    return res

@router.get("/{job_id}", response_model=JobResponse)
async def get_job(
    job_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Job).where(Job.id == job_id, Job.user_id == current_user.id)
    result = await db.execute(stmt)
    j = result.scalars().first()
    if not j:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found.")

    data = StructuredJobData.model_validate(json.loads(j.parsed_data)) if j.parsed_data else None
    return JobResponse(
        id=j.id,
        user_id=j.user_id,
        title=j.title,
        company=j.company,
        location=j.location,
        employment_type=j.employment_type,
        seniority=j.seniority,
        source_url=j.source_url,
        raw_description=j.raw_description,
        parsed_data=data,
        created_at=j.created_at
    )
