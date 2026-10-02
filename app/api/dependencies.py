from sqlalchemy.orm import Session
from fastapi import Depends
from app.infrastructure.database import get_db
from app.infrastructure.repositories.sqlalchemy_task_repository import SQLAlchemyTaskRepository
from app.domain.repositories.task_repository import TaskRepository
from app.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.repositories.sqlalchemy_document_repository import SQLAlchemyDocumentRepository
from app.domain.repositories.document_repository import DocumentRepository


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


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    """
    Dependencia de FastAPI que entrega un UserRepository listo para usar
    a cualquier endpoint que lo necesite.

    Recibe la sesión de base de datos mediante get_db y devuelve la
    interfaz abstracta para que los endpoints no dependan de SQLAlchemy.
    """
    return SQLAlchemyUserRepository(db)


def get_document_repository(db: Session = Depends(get_db)) -> DocumentRepository:
    """
    Dependencia de FastAPI que entrega un DocumentRepository listo para usar
    a cualquier endpoint que lo necesite.

    Recibe la sesión de base de datos mediante get_db y devuelve la
    interfaz abstracta para que los endpoints no dependan de SQLAlchemy.
    """
    return SQLAlchemyDocumentRepository(db)
