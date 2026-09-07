from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User
from app.models.evaluation import Approval
from app.models.resume import ResumeVersion
from app.schemas.evaluator import HumanApprovalRequest
from app.api.deps import get_current_user

router = APIRouter(prefix="/approvals", tags=["Human in the Loop"])

@router.post("", status_code=status.HTTP_200_OK)
async def submit_human_approval(
    payload: HumanApprovalRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    approval = Approval(
        user_id=current_user.id,
        artifact_type=payload.artifact_type,
        artifact_id=payload.artifact_id,
        status=payload.decision,
        user_feedback=payload.feedback,
        final_artifact_content=payload.edited_content
    )
    db.add(approval)

    # If approving a resume version, mark it approved
    if payload.artifact_type == "resume_version":
        v_stmt = select(ResumeVersion).where(ResumeVersion.id == payload.artifact_id)
        version = (await db.execute(v_stmt)).scalars().first()
        if version:
            version.is_approved = (payload.decision == "approve")
            if payload.edited_content:
                version.content = payload.edited_content

    await db.commit()
    return {
        "status": "recorded",
        "artifact_type": payload.artifact_type,
        "artifact_id": payload.artifact_id,
        "decision": payload.decision
    }
