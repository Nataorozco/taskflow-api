from pydantic import BaseModel, Field
from datetime import datetime, timezone
from enum import Enum


class DocumentType(str, Enum):
    """Tipos de documento soportados por el sistema."""
    PDF = "pdf"
    TEXT = "text"
    MARKDOWN = "markdown"
    DOCX = "docx"


class Document(BaseModel):
    """
    Modelo de dominio de un documento (Pydantic puro).
    Su contraparte con SQLAlchemy es DocumentORM.
    """

    id: int | None = None
    title: str

    # Texto ya extraído del documento (no el archivo binario en sí —
    # ese normalmente se guardaría aparte, en disco o en un servicio
    # de almacenamiento; aquí solo referenciamos el contenido de texto).
    content: str

    doc_type: DocumentType

    # Un documento puede pertenecer a una tarea específica, pero no es
    # obligatorio — por ejemplo, un documento general sin tarea asociada.
    task_id: int | None = None

    owner_id: int

    # Empieza vacío a propósito: es el campo que el
    # DocumentSummarizerAgent llena después de procesar el documento.
    summary: str | None = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))