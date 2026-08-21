from pydantic import BaseModel
from datetime import datetime
from app.domain.models.task import TaskStatus, TaskPriority


class TaskCreate(BaseModel):
    """
    Lo que un cliente envía para CREAR una tarea.

    A propósito, deliberadamente limitado: sin id, sin owner_id (vendrá
    de la autenticación más adelante, por ahora fijo), sin created_at
    — esos campos no le corresponde definirlos al cliente, los asigna
    el sistema. Esta separación evita que alguien pueda enviar, por
    ejemplo, {"id": 999, "owner_id": 5} e intentar manipular datos
    que no le pertenecen.
    """
    title: str
    description: str | None = None
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: datetime | None = None


class TaskResponse(BaseModel):
    """
    Lo que la API devuelve al cliente después de crear/consultar una tarea.

    Esta es la forma que se muestra hacia afuera — separada del modelo
    de dominio Task interno (app/domain/models/task.py), aunque ahora
    mismo se vean casi idénticos. Tenerlos separados permite que en el
    futuro cambien de forma independiente: por ejemplo, si el dominio
    interno agrega un campo sensible que nunca debería mostrarse al
    cliente, TaskResponse simplemente no lo incluye.
    """
    id: int
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    owner_id: int
    due_date: datetime | None
    created_at: datetime
    updated_at: datetime | None

    class Config:
        # from_attributes=True permite crear un TaskResponse
        # directamente a partir de un objeto Task de dominio
        # (Pydantic lee sus atributos automáticamente), en vez de
        # tener que desempacar cada campo manualmente uno por uno.
        from_attributes = True