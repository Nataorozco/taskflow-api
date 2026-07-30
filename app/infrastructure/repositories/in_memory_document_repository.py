from app.domain.repositories.document_repository import DocumentRepository
from app.domain.models.document import Document


class InMemoryDocumentRepository(DocumentRepository):
    """
    Implementación en memoria del DocumentRepository.
    """

    def __init__(self):
        self._documents: dict[int, Document] = {}
        self._next_id = 1

    def save(self, document: Document) -> Document:
        if document.id is None:
            document.id = self._next_id
            self._next_id += 1
        self._documents[document.id] = document
        return document

    def get_by_id(self, document_id: int) -> Document | None:
        return self._documents.get(document_id)

    def get_all_by_owner(self, owner_id: int) -> list[Document]:
        return [d for d in self._documents.values() if d.owner_id == owner_id]

    def get_all_by_task(self, task_id: int) -> list[Document]:
        return [d for d in self._documents.values() if d.task_id == task_id]

    def delete(self, document_id: int) -> bool:
        if document_id in self._documents:
            del self._documents[document_id]
            return True
        return False