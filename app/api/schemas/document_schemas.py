from datetime import datetime

from pydantic import BaseModel

from app.domain.models.document import DocumentType


class DocumentCreate(BaseModel):
    """Datos que el cliente envía para crear un documento.

    El cliente aporta el contenido y su tipo; el id, el propietario y
    el resumen pertenecen al sistema y se asignan durante el flujo de la aplicación.
    """
    title: str
    content: str
    doc_type: DocumentType
    task_id: int | None = None


class DocumentResponse(BaseModel):
    """Representación completa de un documento que devuelve la API.

    Incluye summary aunque todavía no se haya generado, porque el resumen
    puede ser None mientras el agente correspondiente no procese el documento.
    """
    id: int
    title: str
    content: str
    doc_type: DocumentType
    task_id: int | None
    owner_id: int
    summary: str | None
    created_at: datetime

    class Config:
        # Permite construir la respuesta directamente desde el modelo
        # de dominio, leyendo sus atributos sin desempacarlos a mano.
        from_attributes = True
