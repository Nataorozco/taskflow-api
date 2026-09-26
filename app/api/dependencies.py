from sqlalchemy.orm import Session
from fastapi import Depends
from app.infrastructure.database import get_db
from app.infrastructure.repositories.sqlalchemy_task_repository import SQLAlchemyTaskRepository
from app.domain.repositories.task_repository import TaskRepository


def get_task_repository(db: Session = Depends(get_db)) -> TaskRepository:
    """
    Dependencia de FastAPI que entrega un TaskRepository listo para usar
    a cualquier endpoint que lo necesite.

    Depends(get_db) le dice a FastAPI: "antes de llamar a esta función,
    primero ejecuta get_db() (definida en database.py) para obtener una
    sesión". FastAPI maneja automáticamente el ciclo de vida completo:
    abre la sesión al iniciar la petición HTTP, se la entrega a esta
    función, y la cierra automáticamente cuando la petición termina
    (incluso si hubo un error) — gracias al patrón yield/finally que
    ya vimos en get_db().

    El tipo de retorno es TaskRepository (la interfaz abstracta), no
    SQLAlchemyTaskRepository (la implementación concreta) — así, si en
    el futuro se quisiera usar otra implementación (por ejemplo, para
    tests), solo habría que cambiar esta función, sin tocar ningún
    endpoint que la use.
    """
    return SQLAlchemyTaskRepository(db)