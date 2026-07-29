from app.infrastructure.repositories.in_memory_task_repository import InMemoryTaskRepository
from app.domain.models.task import Task

repo = InMemoryTaskRepository()

# Crear
task1 = repo.save(Task(title="Primera tarea", owner_id=1))
task2 = repo.save(Task(title="Segunda tarea", owner_id=1))
task3 = repo.save(Task(title="Tarea de otro usuario", owner_id=2))

print("--- Guardadas ---")
print(task1)
print(task2)

print()
print("--- Buscar por id ---")
print(repo.get_by_id(1))

print()
print("--- Todas las del owner 1 ---")
print(repo.get_all_by_owner(1))

print()
print("--- Eliminar tarea 1 ---")
print("Eliminada:", repo.delete(1))
print("Buscar de nuevo:", repo.get_by_id(1))