from sqlalchemy.orm import Session
from app.domain.repositories.task_repository import TaskRepository
from app.domain.models.task import Task
from app.infrastructure.orm_models.task_orm import TaskORM


class SQLAlchemyTaskRepository(TaskRepository):
    """
    Implementación real del TaskRepository, usando SQLAlchemy y Postgres.

    A diferencia de InMemoryTaskRepository, este repositorio no crea
    su propia sesión — la recibe ya abierta desde afuera (ver
    database.py -> get_db()). Esto le da a quien usa el repositorio
    control total sobre cuándo abrir y cerrar la conexión, importante
    cuando se conecte con FastAPI (una sesión por request, no una
    sesión global compartida).
    """

    def __init__(self, db: Session):
        self.db = db

    def save(self, task: Task) -> Task:
        if task.id is None:
            # Crear una tarea nueva: construimos un TaskORM (la
            # representación de fila de tabla) a partir de los datos
            # del Task de dominio, y lo agregamos a la sesión.
            task_orm = TaskORM(
                title=task.title,
                description=task.description,
                status=task.status,
                priority=task.priority,
                owner_id=task.owner_id,
                due_date=task.due_date,
                created_at=task.created_at,
                updated_at=task.updated_at,
            )
            self.db.add(task_orm)
        else:
            # Actualizar una tarea existente: la buscamos primero,
            # y si no existe, es un error real (no un caso silencioso).
            task_orm = self.db.query(TaskORM).filter(TaskORM.id == task.id).first()
            if task_orm is None:
                raise ValueError(f"No existe una tarea con id {task.id}")
            task_orm.title = task.title
            task_orm.description = task.description
            task_orm.status = task.status
            task_orm.priority = task.priority
            task_orm.due_date = task.due_date
            task_orm.updated_at = task.updated_at

        # commit() es lo que realmente escribe el cambio en Postgres
        # (antes de esto, todo queda "pendiente" solo en la sesión).
        self.db.commit()
        # refresh() recarga el objeto desde la base de datos — así
        # obtenemos el id real que Postgres le asignó automáticamente
        # (en el caso de una tarea nueva).
        self.db.refresh(task_orm)
        return self._to_domain(task_orm)

    def get_by_id(self, task_id: int) -> Task | None:
        task_orm = self.db.query(TaskORM).filter(TaskORM.id == task_id).first()
        return self._to_domain(task_orm) if task_orm else None

    def get_all_by_owner(self, owner_id: int) -> list[Task]:
        tasks_orm = self.db.query(TaskORM).filter(TaskORM.owner_id == owner_id).all()
        return [self._to_domain(t) for t in tasks_orm]

    def delete(self, task_id: int) -> bool:
        task_orm = self.db.query(TaskORM).filter(TaskORM.id == task_id).first()
        if task_orm is None:
            return False
        self.db.delete(task_orm)
        self.db.commit()
        return True

    def _to_domain(self, task_orm: TaskORM) -> Task:
        """
        Convierte un TaskORM (fila de la base de datos) en un Task de
        dominio (Pydantic). Esta es la función "traductora" clave del
        repositorio: garantiza que, sin importar qué implementación de
        TaskRepository se use (memoria o Postgres real), el resto del
        sistema siempre recibe un objeto Task limpio, nunca un TaskORM.
        """
        return Task(
            id=task_orm.id,
            title=task_orm.title,
            description=task_orm.description,
            status=task_orm.status,
            priority=task_orm.priority,
            owner_id=task_orm.owner_id,
            due_date=task_orm.due_date,
            created_at=task_orm.created_at,
            updated_at=task_orm.updated_at,
        )