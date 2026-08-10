from app.domain.repositories.task_repository import TaskRepository
from app.domain.models.task import Task


class InMemoryTaskRepository(TaskRepository):
    """
    Implementación en memoria del TaskRepository.

    Útil para tests y desarrollo rápido, sin necesitar una base de
    datos real corriendo. Los datos se pierden al reiniciar el
    programa (viven solo en el diccionario self._tasks mientras el
    proceso de Python está activo). Cumple exactamente el mismo
    contrato que SQLAlchemyTaskRepository — el resto del sistema no
    nota la diferencia entre usar una u otra.
    """

    def __init__(self):
        # Diccionario simple: clave = id de la tarea, valor = la tarea.
        self._tasks: dict[int, Task] = {}
        # Contador manual para simular la auto-asignación de id que
        # normalmente haría una base de datos real.
        self._next_id = 1

    def save(self, task: Task) -> Task:
        if task.id is None:
            # Tarea nueva: le asignamos el siguiente id disponible.
            task.id = self._next_id
            self._next_id += 1
        self._tasks[task.id] = task
        return task

    def get_by_id(self, task_id: int) -> Task | None:
        return self._tasks.get(task_id)

    def get_all_by_owner(self, owner_id: int) -> list[Task]:
        return [t for t in self._tasks.values() if t.owner_id == owner_id]

    def delete(self, task_id: int) -> bool:
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False


