from sqlalchemy.orm import Session
from fastapi import Depends
from app.infrastructure.database import get_db
from app.infrastructure.repositories.sqlalchemy_task_repository import SQLAlchemyTaskRepository
from app.domain.repositories.task_repository import TaskRepository
from app.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.repositories.sqlalchemy_document_repository import SQLAlchemyDocumentRepository
from app.domain.repositories.document_repository import DocumentRepository
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token


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



# OAuth2PasswordBearer le dice a FastAPI cómo esperar el token: en el
# header "Authorization: Bearer <token>". tokenUrl apunta al endpoint
# de login — esto es lo que hace que el botón "Authorize" de /docs
# sepa a dónde enviar las credenciales para obtener un token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)) -> int:
    """
    Dependencia que protege endpoints: exige un token JWT válido y
    devuelve el id del usuario autenticado.

    Cualquier endpoint que incluya esta dependencia (vía
    Depends(get_current_user)) automáticamente:
    1. Exige que la petición traiga un token Bearer
    2. Verifica que el token sea válido y no haya expirado
    3. Si todo está bien, entrega el user_id real — listo para
       reemplazar el TEMP_OWNER_ID fijo que se usaba antes
    """
    user_id = decode_access_token(token)
    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id
