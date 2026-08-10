from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLEnum
from datetime import datetime, timezone
from app.infrastructure.database import Base
from app.domain.models.task import TaskStatus, TaskPriority


class TaskORM(Base):
    """
    Modelo ORM de una tarea — representa la tabla 'tasks' en Postgres.

    IMPORTANTE: esta clase es DISTINTA de Task (Pydantic, en
    app/domain/models/task.py). TaskORM sabe cómo se guarda una tarea
    en la base de datos (columnas, tipos SQL, claves); Task sabe cómo
    se ve una tarea para la lógica de negocio y los agentes. El
    repositorio (SQLAlchemyTaskRepository) es el "traductor" entre
    ambas representaciones.
    """

    __tablename__ = "tasks"

    # primary_key=True: identifica cada fila de forma única.
    # index=True: acelera las búsquedas por id.
    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Reutilizamos los mismos Enum que ya existen en el modelo Pydantic
    # (TaskStatus, TaskPriority), para que los valores válidos sean
    # exactamente los mismos en ambos lados — nunca hay riesgo de que
    # la base de datos acepte un valor que el dominio rechazaría.
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    priority = Column(SQLEnum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)

    # index=True aquí porque get_all_by_owner() va a filtrar por esta
    # columna constantemente — el índice acelera esas consultas a
    # medida que la tabla crezca.
    owner_id = Column(Integer, nullable=False, index=True)

    due_date = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=True)