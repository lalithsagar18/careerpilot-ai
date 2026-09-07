import re
import json
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.document import Document, DocumentChunk
from app.schemas.document import DocumentSearchResult
from app.core.ai_provider import AIProvider, get_ai_provider

class RAGEngine:
    """
    User-scoped Retrieval-Augmented Generation Engine.
    Guarantees strict tenant/user isolation and source attribution.
    """

    CHUNK_SIZE = 500  # words
    CHUNK_OVERLAP = 50 # words

    def __init__(self, ai_provider: AIProvider = None):
        self.ai = ai_provider or get_ai_provider()

    @classmethod
    def chunk_text(cls, text: str) -> List[str]:
        words = text.split()
        if not words:
            return []
        
        chunks = []
        start = 0
        while start < len(words):
            end = min(start + cls.CHUNK_SIZE, len(words))
            chunk_words = words[start:end]
            chunk_str = " ".join(chunk_words)
            if chunk_str.strip():
                chunks.append(chunk_str.strip())
            start += (cls.CHUNK_SIZE - cls.CHUNK_OVERLAP)
        return chunks

    async def ingest_document(
        self,
        db: AsyncSession,
        user_id: str,
        document_id: str,
        text: str,
        metadata: Dict[str, Any] = None
    ) -> int:
        chunks = self.chunk_text(text)
        if not chunks:
            return 0

        # Generate embeddings
        embeddings = await self.ai.generate_embeddings(chunks)

        for i, (chunk_text, emb) in enumerate(zip(chunks, embeddings)):
            chunk_record = DocumentChunk(
                document_id=document_id,
                user_id=user_id,
                chunk_index=i,
                content=chunk_text,
                embedding=emb,
                chunk_metadata=json.dumps(metadata or {})
            )
            db.add(chunk_record)

        await db.commit()
        return len(chunks)

    async def search_user_knowledge(
        self,
        db: AsyncSession,
        user_id: str,
        query: str,
        top_k: int = 4,
        category: Optional[str] = None
    ) -> List[DocumentSearchResult]:
        # Embed query
        query_embeddings = await self.ai.generate_embeddings([query])
        query_vec = query_embeddings[0]

        # Retrieve user chunks only
        stmt = (
            select(DocumentChunk, Document)
            .join(Document, DocumentChunk.document_id == Document.id)
            .where(
                and_(
                    DocumentChunk.user_id == user_id,
                    Document.user_id == user_id
                )
            )
        )
        if category:
            stmt = stmt.where(Document.category == category)

        result = await db.execute(stmt)
        rows = result.all()

        if not rows:
            return []

        # Cosine similarity scoring in memory if vector ops unavailable, or direct ranking
        scored_results = []
        for chunk, doc in rows:
            chunk_emb = chunk.embedding
            # If embedding is a list of floats
            if isinstance(chunk_emb, list) and len(chunk_emb) == len(query_vec):
                dot_product = sum(a * b for a, b in zip(query_vec, chunk_emb))
                score = round(max(0.0, min(1.0, (dot_product + 1.0) / 2.0)), 4)
            else:
                score = 0.5  # fallback baseline
            
            meta = json.loads(chunk.chunk_metadata) if chunk.chunk_metadata else {}
            scored_results.append(
                DocumentSearchResult(
                    document_id=doc.id,
                    document_title=doc.title,
                    category=doc.category,
                    chunk_index=chunk.chunk_index,
                    content=chunk.content,
                    similarity_score=score,
                    metadata=meta
                )
            )

        # Sort descending by similarity
        scored_results.sort(key=lambda x: x.similarity_score, reverse=True)
        return scored_results[:top_k]
