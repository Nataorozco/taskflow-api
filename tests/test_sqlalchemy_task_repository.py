from app.infrastructure.database import SessionLocal
from app.infrastructure.repositories.sqlalchemy_task_repository import SQLAlchemyTaskRepository
from app.domain.models.task import Task, TaskPriority

db = SessionLocal()
repo = SQLAlchemyTaskRepository(db)

# Crear
task = repo.save(Task(
    title="Probar SQLAlchemyTaskRepository",
    description="Confirmar que se guarda de verdad en Postgres",
    priority=TaskPriority.HIGH,
    owner_id=1
))
print("--- Guardada ---")
print(task)

# Buscar por id
print()
print("--- Buscar por id ---")
print(repo.get_by_id(task.id))

# Listar por owner
print()
print("--- Todas del owner 1 ---")
print(repo.get_all_by_owner(1))

db.close()