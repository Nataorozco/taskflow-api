from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Datos que el cliente envía para crear una cuenta.

    El cliente aporta la contraseña en texto plano para que el sistema
    la procese; los campos internos como id, estado y fecha de creación
    los asigna la aplicación.
    """
    email: EmailStr
    full_name: str
    password: str


class UserResponse(BaseModel):
    """Datos públicos de un usuario, sin incluir información sensible.

    Mantener este schema separado del modelo de dominio evita exponer
    el hash de la contraseña aunque el objeto interno lo contenga.
    """
    id: int
    email: EmailStr
    full_name: str
    is_active: bool
    created_at: datetime

    class Config:
        # Permite construir la respuesta directamente desde el modelo
        # de dominio, leyendo sus atributos sin desempacarlos a mano.
        from_attributes = True
