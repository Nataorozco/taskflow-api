from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_user_repository
from app.api.schemas.user_schemas import UserCreate, UserResponse
from app.domain.models.user import User
from app.domain.repositories.user_repository import UserRepository
from app.core.security import hash_password


# Agrupa las rutas de usuarios bajo /users para que la aplicación
# principal pueda montarlas junto con los demás recursos.
router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
def create_user(
    user_data: UserCreate,
    repo: UserRepository = Depends(get_user_repository),
):
    """Crea una cuenta y devuelve únicamente sus datos públicos.

    El hash simulado mantiene la contraseña en un campo interno que no
    sale por la API; el algoritmo seguro se incorporará con autenticación.
    """
    user = User(
            email=user_data.email,
            full_name=user_data.full_name,
            hashed_password=hash_password(user_data.password),
        )
    
    return repo.save(user)
    


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    repo: UserRepository = Depends(get_user_repository),
):
    """Busca un usuario por id y responde 404 si no existe.

    El error explícito evita que un id inexistente parezca una consulta
    exitosa con un resultado vacío.
    """
    user = repo.get_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    repo: UserRepository = Depends(get_user_repository),
):
    """Elimina un usuario y devuelve 404 cuando no se encontró.

    Así el cliente puede distinguir una eliminación real de un id que
    nunca existió, en lugar de recibir un éxito silencioso.
    """
    deleted = repo.delete(user_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"success": True, "message": f"Usuario {user_id} eliminado"}
