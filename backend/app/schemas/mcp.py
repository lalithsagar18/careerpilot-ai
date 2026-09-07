from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class MCPToolDefinition(BaseModel):
    name: str
    description: str
    inputSchema: Dict[str, Any]

class MCPToolCallRequest(BaseModel):
    tool: str
    parameters: Dict[str, Any] = Field(default_factory=dict)

class MCPToolCallResponse(BaseModel):
    tool: str
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
