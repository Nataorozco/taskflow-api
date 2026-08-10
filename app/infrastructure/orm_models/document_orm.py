from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from datetime import datetime, timezone
from app.infrastructure.database import Base
from app.domain.models.document import DocumentType


class DocumentORM(Base):
    """
    Modelo ORM de un documento — representa la tabla 'documents' en Postgres.
    """

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    doc_type = Column(SQLEnum(DocumentType), nullable=False)

    # task_id es un Integer simple (no una relación formal con
    # ForeignKey hacia la tabla 'tasks' todavía) — por simplicidad,
    # manteniendo consistencia con el modelo Pydantic. Se puede
    # formalizar como relación real más adelante si se necesita.
    task_id = Column(Integer, nullable=True, index=True)

    owner_id = Column(Integer, nullable=False, index=True)
    summary = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))