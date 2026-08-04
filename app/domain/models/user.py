from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, timezone


class User(BaseModel):
    """
    Modelo de dominio de un usuario (Pydantic puro).

    Igual que Task, esta clase no sabe nada de bases de datos.
    Su contraparte con SQLAlchemy es UserORM, en
    app/infrastructure/orm_models/user_orm.py.
    """

    id: int | None = None

    # EmailStr valida automáticamente el formato del correo
    # (requiere el paquete pydantic[email] instalado).
    email: EmailStr

    full_name: str

    # NUNCA se guarda la contraseña en texto plano, ni siquiera aquí,
    # en el modelo interno. Este campo contiene el resultado de un
    # algoritmo de hash (ej. bcrypt), no la contraseña real del usuario.
    hashed_password: str

    # Permite "desactivar" una cuenta sin borrar sus datos ni su historial.
    is_active: bool = True

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))