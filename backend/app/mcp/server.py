import logging
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.schemas.mcp import MCPToolDefinition, MCPToolCallResponse
from app.models.user import User
from app.models.resume import Resume
from app.models.job import Job
from app.models.skill_gap import SkillGap
from app.models.interview import Interview
from app.tools.scoring_engine import DeterministicScoringEngine
from app.rag.engine import RAGEngine
from app.schemas.resume import CandidateProfile
from app.schemas.job import StructuredJobData
import json

logger = logging.getLogger("careerpilot.mcp")

class MCPServer:
    """
    Model Context Protocol Server for CareerPilot AI.
    Exposes typed, user-scoped tools over JSON-RPC 2.0.
    """

    TOOLS: List[MCPToolDefinition] = [
        MCPToolDefinition(
            name="get_candidate_profile",
            description="Retrieve the authenticated candidate's structured profile including verified skills and experience.",
            inputSchema={"type": "object", "properties": {"resume_id": {"type": "string"}}, "required": []}
        ),
        MCPToolDefinition(
            name="calculate_job_match",
            description="Deterministically calculate 6-dimension match score and skill gaps between a resume and job posting.",
            inputSchema={"type": "object", "properties": {"resume_id": {"type": "string"}, "job_id": {"type": "string"}}, "required": ["resume_id", "job_id"]}
        ),
        MCPToolDefinition(
            name="search_career_documents",
            description="Perform grounded vector similarity search over the user's uploaded career knowledge documents.",
            inputSchema={"type": "object", "properties": {"query": {"type": "string"}, "top_k": {"type": "integer"}}, "required": ["query"]}
        ),
        MCPToolDefinition(
            name="get_interview_history",
            description="Retrieve previous mock interview scores, transcripts, and identified weaknesses for targeted practice.",
            inputSchema={"type": "object", "properties": {"limit": {"type": "integer"}}, "required": []}
        )
    ]

    @classmethod
    def list_tools(cls) -> List[MCPToolDefinition]:
        return cls.TOOLS

    @classmethod
    async def execute_tool(
        cls,
        tool_name: str,
        parameters: Dict[str, Any],
        user: User,
        db: AsyncSession
    ) -> MCPToolCallResponse:
        logger.info(f"MCP execute tool '{tool_name}' for user {user.id}")

        try:
            if tool_name == "get_candidate_profile":
                resume_id = parameters.get("resume_id")
                stmt = select(Resume).where(Resume.user_id == user.id)
                if resume_id:
                    stmt = stmt.where(Resume.id == resume_id)
                result = await db.execute(stmt)
                resume = result.scalars().first()
                if not resume or not resume.candidate_profile:
                    return MCPToolCallResponse(tool=tool_name, success=False, error="No parsed candidate profile found.")
                return MCPToolCallResponse(tool=tool_name, success=True, result=json.loads(resume.candidate_profile))

            elif tool_name == "calculate_job_match":
                resume_id = parameters.get("resume_id")
                job_id = parameters.get("job_id")
                
                # Fetch resume
                res_stmt = select(Resume).where(Resume.id == resume_id, Resume.user_id == user.id)
                res_row = (await db.execute(res_stmt)).scalars().first()
                # Fetch job
                job_stmt = select(Job).where(Job.id == job_id, Job.user_id == user.id)
                job_row = (await db.execute(job_stmt)).scalars().first()

                if not res_row or not job_row or not res_row.candidate_profile or not job_row.parsed_data:
                    return MCPToolCallResponse(tool=tool_name, success=False, error="Invalid resume_id or job_id, or profiles not yet structured.")

                cand = CandidateProfile.model_validate(json.loads(res_row.candidate_profile))
                job_data = StructuredJobData.model_validate(json.loads(job_row.parsed_data))

                breakdown, matched, missing, partial = DeterministicScoringEngine.calculate_match(cand, job_data)
                return MCPToolCallResponse(
                    tool=tool_name, 
                    success=True, 
                    result={
                        "score_breakdown": breakdown.model_dump(),
                        "matched_skills": [m.model_dump() for m in matched],
                        "missing_skills": [m.model_dump() for m in missing],
                        "partial_skills": [p.model_dump() for p in partial]
                    }
                )

            elif tool_name == "search_career_documents":
                query = parameters.get("query", "")
                top_k = parameters.get("top_k", 4)
                rag_engine = RAGEngine()
                results = await rag_engine.search_user_knowledge(db=db, user_id=user.id, query=query, top_k=top_k)
                return MCPToolCallResponse(tool=tool_name, success=True, result=[r.model_dump() for r in results])

            elif tool_name == "get_interview_history":
                limit = parameters.get("limit", 5)
                stmt = select(Interview).where(Interview.user_id == user.id).order_by(Interview.created_at.desc()).limit(limit)
                rows = (await db.execute(stmt)).scalars().all()
                interviews_data = []
                for r in rows:
                    interviews_data.append({
                        "id": r.id,
                        "target_role": r.target_role,
                        "interview_type": r.interview_type,
                        "overall_score": r.overall_score,
                        "status": r.status,
                        "weaknesses": json.loads(r.weaknesses) if r.weaknesses else [],
                    })
                return MCPToolCallResponse(tool=tool_name, success=True, result=interviews_data)

            else:
                return MCPToolCallResponse(tool=tool_name, success=False, error=f"Unknown tool '{tool_name}'")

        except Exception as e:
            logger.error(f"Error in MCP tool '{tool_name}': {e}", exc_info=True)
            return MCPToolCallResponse(tool=tool_name, success=False, error=str(e))
