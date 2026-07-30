from app.infrastructure.repositories.in_memory_document_repository import InMemoryDocumentRepository
from app.domain.models.document import Document, DocumentType

repo = InMemoryDocumentRepository()

doc1 = repo.save(Document(
    title="Especificación del proyecto",
    content="Contenido de ejemplo...",
    doc_type=DocumentType.MARKDOWN,
    owner_id=1,
    task_id=5
))
doc2 = repo.save(Document(
    title="Notas generales",
    content="Otro contenido...",
    doc_type=DocumentType.TEXT,
    owner_id=1
))

print("--- Guardados ---")
print(doc1)
print(doc2)

print()
print("--- Por owner 1 ---")
print(repo.get_all_by_owner(1))

print()
print("--- Por task 5 ---")
print(repo.get_all_by_task(5))

print()
print("--- Eliminar doc 1 ---")
print("Eliminado:", repo.delete(1))
print("Buscar de nuevo:", repo.get_by_id(1))