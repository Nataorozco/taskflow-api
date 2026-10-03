from pydantic import BaseModel


class LoginRequest(BaseModel):
    """
    Datos que el cliente envía para iniciar sesión.
    Deliberadamente simple: solo lo necesario para identificar al
    usuario y verificar su contraseña.
    """
    email: str
    password: str


class TokenResponse(BaseModel):
    """
    Lo que la API devuelve tras un login exitoso.

    access_token: el JWT que el cliente debe guardar y enviar en
    futuras peticiones (normalmente en el header Authorization).

    token_type: "bearer" es el estándar — le indica al cliente cómo
    debe enviar el token: "Authorization: Bearer <token>".
    """
    access_token: str
    token_type: str = "bearer"