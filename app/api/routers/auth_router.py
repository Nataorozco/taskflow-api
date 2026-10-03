from fastapi import APIRouter, Depends, HTTPException
from app.api.schemas.auth_schemas import LoginRequest, TokenResponse
from app.api.dependencies import get_user_repository
from app.domain.repositories.user_repository import UserRepository
from app.core.security import verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=TokenResponse)
def login(
    credentials: LoginRequest,
    repo: UserRepository = Depends(get_user_repository)
):
    """
    Verifica email y contraseña, y devuelve un token de acceso si son
    correctos.

    Por seguridad, el mensaje de error es el mismo tanto si el email
    no existe como si la contraseña es incorrecta ("Credenciales
    inválidas") — nunca se distingue cuál de las dos cosas falló.
    Si el error dijera específicamente "email no encontrado", alguien
    podría usar ese endpoint para averiguar qué emails están
    registrados en el sistema, probando uno por uno.
    """
    user = repo.get_by_email(credentials.email)

    if user is None or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    access_token = create_access_token(user_id=user.id)
    return TokenResponse(access_token=access_token)