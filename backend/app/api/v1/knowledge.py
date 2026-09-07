from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.user import User
from app.models.document import Document
from app.schemas.document import DocumentResponse, DocumentSearchRequest, DocumentSearchResult, GroundedQARequest, GroundedQAResponse
from app.api.deps import get_current_user
from app.tools.document_extractor import DocumentExtractor
from app.rag.engine import RAGEngine
from app.agents.rag_agent import RAGKnowledgeAgent
from app.core.config import settings

router = APIRouter(prefix="/knowledge", tags=["Career Knowledge & RAG"])

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    category: str = Form("general"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File exceeds limit of {settings.MAX_UPLOAD_SIZE_BYTES // (1024*1024)}MB."
        )

    text = DocumentExtractor.extract_text_from_bytes(content, file.filename or "doc.txt")
    if not text.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Could not extract text from document.")

    doc = Document(
        user_id=current_user.id,
        title=title,
        file_name=file.filename or "document.txt",
        file_type=file.filename.split(".")[-1].lower() if "." in file.filename else "txt",
        category=category,
        file_size_bytes=len(content),
        summary=text[:300] + "..."
    )
    db.add(doc)
    await db.commit()
    await db.refresh(doc)

    # Ingest chunks & embeddings
    rag = RAGEngine()
    await rag.ingest_document(
        db=db,
        user_id=current_user.id,
        document_id=doc.id,
        text=text,
        metadata={"title": title, "category": category, "file_name": doc.file_name}
    )

    return DocumentResponse.model_validate(doc)

@router.get("", response_model=List[DocumentResponse])
async def list_documents(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Document).where(Document.user_id == current_user.id).order_by(Document.created_at.desc())
    docs = (await db.execute(stmt)).scalars().all()
    return [DocumentResponse.model_validate(d) for d in docs]

@router.post("/search", response_model=List[DocumentSearchResult])
async def search_documents(
    payload: DocumentSearchRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    rag = RAGEngine()
    return await rag.search_user_knowledge(
        db=db,
        user_id=current_user.id,
        query=payload.query,
        top_k=payload.top_k,
        category=payload.category
    )

@router.post("/qa", response_model=GroundedQAResponse)
async def grounded_qa(
    payload: GroundedQARequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    rag = RAGEngine()
    sources = await rag.search_user_knowledge(
        db=db,
        user_id=current_user.id,
        query=payload.query,
        top_k=payload.top_k
    )
    agent = RAGKnowledgeAgent()
    return await agent.answer_grounded_query(query=payload.query, retrieved_sources=sources)
