from abc import ABC, abstractmethod
from app.domain.models.task import Task


class TaskRepository(ABC):
    """
    Contrato abstracto para persistir y consultar tareas.
    El dominio depende de esta interfaz, no de una base de datos específica.
    Cualquier implementación (SQLAlchemy, en memoria, etc.) debe cumplir este contrato.
    """

    @abstractmethod
    def save(self, task: Task) -> Task:
        """Crea o actualiza una tarea. Devuelve la tarea guardada (con id asignado)."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, task_id: int) -> Task | None:
        """Busca una tarea por su id. Devuelve None si no existe."""
        raise NotImplementedError

    @abstractmethod
    def get_all_by_owner(self, owner_id: int) -> list[Task]:
        """Devuelve todas las tareas de un usuario específico."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        """Elimina una tarea. Devuelve True si se eliminó, False si no existía."""
        raise NotImplementedError