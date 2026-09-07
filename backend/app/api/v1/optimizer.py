import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User
from app.models.resume import Resume, ResumeVersion
from app.models.job import Job
from app.schemas.optimizer import ResumeOptimizationRequest, ResumeOptimizationResponse
from app.schemas.resume import CandidateProfile
from app.schemas.job import StructuredJobData
from app.api.deps import get_current_user
from app.agents.optimizer_agent import ResumeOptimizationAgent

router = APIRouter(prefix="/optimize", tags=["Resume Optimization"])

@router.post("", response_model=ResumeOptimizationResponse)
async def optimize_resume(
    payload: ResumeOptimizationRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Retrieve resume
    res_stmt = select(Resume).where(Resume.id == payload.resume_id, Resume.user_id == current_user.id)
    resume = (await db.execute(res_stmt)).scalars().first()
    if not resume or not resume.candidate_profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found or not parsed.")

    # Retrieve job
    job_stmt = select(Job).where(Job.id == payload.job_id, Job.user_id == current_user.id)
    job = (await db.execute(job_stmt)).scalars().first()
    if not job or not job.parsed_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job posting not found or not parsed.")

    cand = CandidateProfile.model_validate(json.loads(resume.candidate_profile))
    job_data = StructuredJobData.model_validate(json.loads(job.parsed_data))

    agent = ResumeOptimizationAgent()
    opt_result = await agent.optimize_resume(
        candidate=cand,
        job=job_data,
        custom_instructions=payload.custom_instructions
    )

    # Count existing versions to increment version_number
    v_stmt = select(ResumeVersion).where(ResumeVersion.resume_id == resume.id)
    existing_versions = (await db.execute(v_stmt)).scalars().all()
    next_ver = len(existing_versions) + 1

    # Save as pending approval version
    version_record = ResumeVersion(
        resume_id=resume.id,
        version_number=next_ver,
        target_job_id=job.id,
        content=opt_result.full_optimized_content,
        profile_data=json.dumps(cand.model_dump()),
        ats_score=opt_result.ats_score_projected,
        ats_feedback=json.dumps({
            "before": opt_result.ats_score_before,
            "projected": opt_result.ats_score_projected,
            "keywords": opt_result.targeted_keywords_matched,
            "rewrites": [r.model_dump() for r in opt_result.bullet_rewrites]
        }),
        change_summary=f"Optimized for {job.title} at {job.company} (v{next_ver})",
        is_approved=False
    )
    db.add(version_record)
    await db.commit()

    return opt_result
