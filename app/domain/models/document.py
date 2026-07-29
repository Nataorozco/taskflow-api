from pydantic import BaseModel, Field
from datetime import datetime, timezone
from enum import Enum


class DocumentType(str, Enum):
    PDF = "pdf"
    TEXT = "text"
    MARKDOWN = "markdown"
    DOCX = "docx"


class Document(BaseModel):
    id: int | None = None
    title: str
    content: str
    doc_type: DocumentType
    task_id: int | None = None
    owner_id: int
    summary: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))