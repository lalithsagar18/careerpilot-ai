from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict

class DocumentResponse(BaseModel):
    id: str
    user_id: str
    title: str
    file_name: str
    file_type: str
    category: str
    file_size_bytes: int
    summary: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class DocumentSearchRequest(BaseModel):
    query: str = Field(..., min_length=2)
    top_k: int = Field(default=4, ge=1, le=20)
    category: Optional[str] = None

class DocumentSearchResult(BaseModel):
    document_id: str
    document_title: str
    category: str
    chunk_index: int
    content: str
    similarity_score: float
    metadata: Optional[Dict[str, Any]] = None

class GroundedQARequest(BaseModel):
    query: str = Field(..., min_length=2)
    top_k: int = Field(default=4, ge=1, le=10)

class GroundedQAResponse(BaseModel):
    query: str
    answer: str
    grounded: bool
    sources: List[DocumentSearchResult]
