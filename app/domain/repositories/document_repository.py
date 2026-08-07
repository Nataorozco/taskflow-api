from abc import ABC, abstractmethod
from app.domain.models.document import Document


class DocumentRepository(ABC):
    """
    Contrato abstracto para persistir y consultar documentos.
    """

    @abstractmethod
    def save(self, document: Document) -> Document:
        """Crea o actualiza un documento. Devuelve el documento guardado (con id asignado)."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, document_id: int) -> Document | None:
        """Busca un documento por su id. Devuelve None si no existe."""
        raise NotImplementedError

    @abstractmethod
    def get_all_by_owner(self, owner_id: int) -> list[Document]:
        """Devuelve todos los documentos de un usuario específico."""
        raise NotImplementedError

    @abstractmethod
    def get_all_by_task(self, task_id: int) -> list[Document]:
        """
        Devuelve todos los documentos asociados a una tarea específica.
        Existe porque, según el modelo de dominio, un Document puede
        tener un task_id opcional — este método permite responder
        "¿qué documentos tiene esta tarea?" de forma directa.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, document_id: int) -> bool:
        """Elimina un documento. Devuelve True si se eliminó, False si no existía."""
        raise NotImplementedError