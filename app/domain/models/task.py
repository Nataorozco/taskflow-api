from pydantic import BaseModel, Field
from datetime import datetime, timezone
from enum import Enum


class TaskStatus(str, Enum):
    """
    Estados posibles de una tarea.
    Heredar de (str, Enum) permite que el valor se comporte como texto
    (útil para JSON, bases de datos, y comparaciones), pero restringido
    solo a estos 3 valores válidos — evita errores como "Pendiente" o "PENDING".
    """
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TaskPriority(str, Enum):
    """Niveles de prioridad de una tarea. Mismo principio que TaskStatus."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Task(BaseModel):
    """
    Modelo de dominio de una tarea (Pydantic puro).

    IMPORTANTE: esta clase no sabe nada de bases de datos ni de SQLAlchemy.
    Es la representación que usan los agentes y la lógica de negocio.
    La versión que sí conoce Postgres es TaskORM, en
    app/infrastructure/orm_models/task_orm.py — son dos clases separadas
    a propósito (principio de Clean Architecture).
    """

    # id es None cuando la tarea todavía no existe en la base de datos;
    # la base de datos se lo asigna automáticamente al guardarla.
    id: int | None = None

    title: str
    description: str | None = None

    status: TaskStatus = TaskStatus.PENDING
    priority: TaskPriority = TaskPriority.MEDIUM

    # Toda tarea debe pertenecer a un usuario — por eso no tiene valor
    # por defecto, es un campo obligatorio.
    owner_id: int

    # Fecha límite opcional; el ReminderAgent la usa para calcular
    # si una tarea necesita un recordatorio pronto.
    due_date: datetime | None = None

    # default_factory en vez de un valor fijo: si escribiéramos
    # `datetime.now(timezone.utc)` directamente, Pydantic calcularía esa
    # fecha una sola vez al cargar el archivo, no cada vez que se crea
    # una tarea nueva. El lambda asegura que se recalcule en cada creación.
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None