from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from datetime import datetime, timezone
from app.infrastructure.database import Base
from app.domain.models.document import DocumentType


class DocumentORM(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    doc_type = Column(SQLEnum(DocumentType), nullable=False)
    task_id = Column(Integer, nullable=True, index=True)
    owner_id = Column(Integer, nullable=False, index=True)
    summary = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))