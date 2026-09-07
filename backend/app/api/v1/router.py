from fastapi import APIRouter

from app.api.v1.health import router as health_router
from app.api.v1.auth import router as auth_router
from app.api.v1.resumes import router as resumes_router
from app.api.v1.jobs import router as jobs_router
from app.api.v1.match import router as match_router
from app.api.v1.optimizer import router as optimizer_router
from app.api.v1.cover_letters import router as cover_letters_router
from app.api.v1.interviews import router as interviews_router
from app.api.v1.knowledge import router as knowledge_router
from app.api.v1.learning_plans import router as learning_plans_router
from app.api.v1.applications import router as applications_router
from app.api.v1.approvals import router as approvals_router
from app.api.v1.mcp_router import router as mcp_router
from app.api.v1.dashboard import router as dashboard_router

api_v1_router = APIRouter()

api_v1_router.include_router(health_router)
api_v1_router.include_router(auth_router)
api_v1_router.include_router(dashboard_router)
api_v1_router.include_router(resumes_router)
api_v1_router.include_router(jobs_router)
api_v1_router.include_router(match_router)
api_v1_router.include_router(optimizer_router)
api_v1_router.include_router(cover_letters_router)
api_v1_router.include_router(interviews_router)
api_v1_router.include_router(knowledge_router)
api_v1_router.include_router(learning_plans_router)
api_v1_router.include_router(applications_router)
api_v1_router.include_router(approvals_router)
api_v1_router.include_router(mcp_router)
