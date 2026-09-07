import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User
from app.models.resume import Resume, ResumeVersion
from app.schemas.resume import ResumeResponse, ResumeVersionResponse, CandidateProfile, ResumeQualityAssessment
from app.api.deps import get_current_user
from app.tools.document_extractor import DocumentExtractor
from app.agents.resume_agent import ResumeIntelligenceAgent
from app.core.config import settings

router = APIRouter(prefix="/resumes", tags=["Resumes"])

@router.post("/upload", response_model=ResumeResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    title: str = Form("My Resume"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File exceeds maximum allowed size of {settings.MAX_UPLOAD_SIZE_BYTES // (1024*1024)}MB."
        )

    # Extract text
    raw_text = DocumentExtractor.extract_text_from_bytes(content, file.filename or "resume.pdf")
    if not raw_text or len(raw_text.strip()) < 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not extract readable text from resume. Please ensure the document is not an empty or password-protected file."
        )

    # Agent structuring & quality assessment
    agent = ResumeIntelligenceAgent()
    profile = await agent.parse_resume(raw_text)
    assessment = await agent.assess_resume_quality(raw_text, profile)

    resume = Resume(
        user_id=current_user.id,
        title=title,
        file_name=file.filename or "resume.pdf",
        file_type=file.filename.split(".")[-1].lower() if "." in file.filename else "pdf",
        file_size_bytes=len(content),
        raw_text=raw_text,
        candidate_profile=json.dumps(profile.model_dump()),
        health_score=assessment.overall_health_score,
        health_assessment=json.dumps(assessment.model_dump())
    )
    db.add(resume)
    await db.commit()
    await db.refresh(resume)

    return ResumeResponse(
        id=resume.id,
        user_id=resume.user_id,
        title=resume.title,
        file_name=resume.file_name,
        file_type=resume.file_type,
        file_size_bytes=resume.file_size_bytes,
        health_score=resume.health_score,
        candidate_profile=profile,
        health_assessment=assessment,
        created_at=resume.created_at,
        updated_at=resume.updated_at
    )

@router.get("", response_model=List[ResumeResponse])
async def list_resumes(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Resume).where(Resume.user_id == current_user.id).order_by(Resume.created_at.desc())
    result = await db.execute(stmt)
    resumes = result.scalars().all()

    response_list = []
    for r in resumes:
        prof = CandidateProfile.model_validate(json.loads(r.candidate_profile)) if r.candidate_profile else None
        assess = ResumeQualityAssessment.model_validate(json.loads(r.health_assessment)) if r.health_assessment else None
        response_list.append(ResumeResponse(
            id=r.id,
            user_id=r.user_id,
            title=r.title,
            file_name=r.file_name,
            file_type=r.file_type,
            file_size_bytes=r.file_size_bytes,
            health_score=r.health_score,
            candidate_profile=prof,
            health_assessment=assess,
            created_at=r.created_at,
            updated_at=r.updated_at
        ))
    return response_list

@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    resume_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Resume).where(Resume.id == resume_id, Resume.user_id == current_user.id)
    result = await db.execute(stmt)
    r = result.scalars().first()
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resume not found.")

    prof = CandidateProfile.model_validate(json.loads(r.candidate_profile)) if r.candidate_profile else None
    assess = ResumeQualityAssessment.model_validate(json.loads(r.health_assessment)) if r.health_assessment else None
    return ResumeResponse(
        id=r.id,
        user_id=r.user_id,
        title=r.title,
        file_name=r.file_name,
        file_type=r.file_type,
        file_size_bytes=r.file_size_bytes,
        health_score=r.health_score,
        candidate_profile=prof,
        health_assessment=assess,
        created_at=r.created_at,
        updated_at=r.updated_at
    )
