from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User
from app.models.application import Application
from app.schemas.application import ApplicationCreate, ApplicationUpdate, ApplicationResponse
from app.api.deps import get_current_user

router = APIRouter(prefix="/applications", tags=["Job Applications"])

@router.post("", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
async def create_application(
    payload: ApplicationCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    app = Application(
        user_id=current_user.id,
        job_id=payload.job_id,
        resume_version_id=payload.resume_version_id,
        company=payload.company,
        role_title=payload.role_title,
        status=payload.status,
        applied_date=payload.applied_date,
        cover_letter_text=payload.cover_letter_text,
        notes=payload.notes,
        salary_offered=payload.salary_offered
    )
    db.add(app)
    await db.commit()
    await db.refresh(app)
    return ApplicationResponse.model_validate(app)

@router.get("", response_model=List[ApplicationResponse])
async def list_applications(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Application).where(Application.user_id == current_user.id).order_by(Application.updated_at.desc())
    apps = (await db.execute(stmt)).scalars().all()
    return [ApplicationResponse.model_validate(a) for a in apps]

@router.patch("/{application_id}", response_model=ApplicationResponse)
async def update_application(
    application_id: str,
    payload: ApplicationUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Application).where(Application.id == application_id, Application.user_id == current_user.id)
    app = (await db.execute(stmt)).scalars().first()
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found.")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(app, field, value)

    await db.commit()
    await db.refresh(app)
    return ApplicationResponse.model_validate(app)

@router.delete("/{application_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_application(
    application_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Application).where(Application.id == application_id, Application.user_id == current_user.id)
    app = (await db.execute(stmt)).scalars().first()
    if not app:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found.")

    await db.delete(app)
    await db.commit()
    return None
