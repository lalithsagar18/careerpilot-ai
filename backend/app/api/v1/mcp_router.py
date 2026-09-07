from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.schemas.mcp import MCPToolDefinition, MCPToolCallRequest, MCPToolCallResponse
from app.api.deps import get_current_user
from app.mcp.server import MCPServer

router = APIRouter(prefix="/mcp", tags=["Model Context Protocol"])

@router.get("/tools", response_model=List[MCPToolDefinition])
async def list_mcp_tools():
    return MCPServer.list_tools()

@router.post("/execute", response_model=MCPToolCallResponse)
async def execute_mcp_tool(
    payload: MCPToolCallRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return await MCPServer.execute_tool(
        tool_name=payload.tool,
        parameters=payload.parameters,
        user=current_user,
        db=db
    )
