from abc import ABC, abstractmethod
from app.domain.models.task import Task


class TaskRepository(ABC):
    """
    Contrato abstracto para persistir y consultar tareas.

    El dominio depende de esta interfaz, no de una base de datos
    específica — es el principio central de Clean Architecture aplicado
    aquí. Cualquier implementación (SQLAlchemyTaskRepository,
    InMemoryTaskRepository, o incluso una futura versión con MongoDB)
    debe cumplir exactamente este mismo contrato, para que el resto
    del sistema pueda usar cualquiera de ellas sin notar la diferencia.
    """

    @abstractmethod
    def save(self, task: Task) -> Task:
        """
        Crea o actualiza una tarea. Devuelve la tarea guardada (con id
        asignado). Un solo método sirve para ambos casos: si task.id
        es None, se asume creación; si ya tiene id, se asume actualización
        — así se evita duplicar la interfaz con create() y update() separados.
        """
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, task_id: int) -> Task | None:
        """Busca una tarea por su id. Devuelve None si no existe."""
        raise NotImplementedError

    @abstractmethod
    def get_all_by_owner(self, owner_id: int) -> list[Task]:
        """
        Devuelve todas las tareas de un usuario específico. Existe este
        método (y no un get_all() genérico) porque, por diseño, las
        tareas de un usuario nunca deberían mezclarse con las de otro.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        """Elimina una tarea. Devuelve True si se eliminó, False si no existía."""
        raise NotImplementedError