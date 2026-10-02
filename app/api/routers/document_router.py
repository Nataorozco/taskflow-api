from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_document_repository
from app.api.schemas.document_schemas import DocumentCreate, DocumentResponse
from app.domain.models.document import Document
from app.domain.repositories.document_repository import DocumentRepository


# Agrupa las rutas de documentos bajo /documents para que la aplicación
# principal pueda montarlas junto con los demás recursos.
router = APIRouter(prefix="/documents", tags=["documents"])

# TEMPORAL: hasta que exista autenticación real, todos los documentos se
# asignan a este owner_id fijo. Cuando se implemente login/JWT, esto
# se reemplaza por el id del usuario autenticado en cada petición.
TEMP_OWNER_ID = 1


@router.post("/", response_model=DocumentResponse)
def create_document(
    document_data: DocumentCreate,
    repo: DocumentRepository = Depends(get_document_repository),
):
    """Crea un documento y agrega el propietario que el cliente no envía.

    El schema limita la entrada a los datos que aporta el cliente; los
    campos internos quedan bajo control de la aplicación.
    """
    document = Document(
        title=document_data.title,
        content=document_data.content,
        doc_type=document_data.doc_type,
        task_id=document_data.task_id,
        owner_id=TEMP_OWNER_ID,
    )
    return repo.save(document)


@router.get("/by-task/{task_id}", response_model=list[DocumentResponse])
def list_documents_by_task(
    task_id: int,
    repo: DocumentRepository = Depends(get_document_repository),
):
    """Lista los documentos asociados a una tarea específica.

    Esta ruta está antes de la ruta con {document_id} para que el segmento
    fijo "by-task" se interprete como tal y no como un identificador.
    """
    return repo.get_all_by_task(task_id)


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    repo: DocumentRepository = Depends(get_document_repository),
):
    """Busca un documento por id y responde 404 si no existe.

    El error explícito evita que un id inexistente parezca una consulta
    exitosa con un resultado vacío.
    """
    document = repo.get_by_id(document_id)
    if document is None:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return document


@router.get("/", response_model=list[DocumentResponse])
def list_documents(
    repo: DocumentRepository = Depends(get_document_repository),
):
    """Lista todos los documentos del usuario actual (TEMP_OWNER_ID por ahora)."""
    return repo.get_all_by_owner(TEMP_OWNER_ID)


@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    repo: DocumentRepository = Depends(get_document_repository),
):
    """Elimina un documento y devuelve 404 cuando no se encontró.

    Así el cliente puede distinguir una eliminación real de un id que
    nunca existió, en lugar de recibir un éxito silencioso.
    """
    deleted = repo.delete(document_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Documento no encontrado")
    return {"success": True, "message": f"Documento {document_id} eliminado"}
