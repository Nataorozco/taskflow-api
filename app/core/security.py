import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def hash_password(plain_password: str) -> str:
    """
    Convierte una contraseña en texto plano en un hash seguro con bcrypt.

    bcrypt genera automáticamente una "sal" (datos aleatorios) distinta
    cada vez, por eso dos usuarios con la misma contraseña nunca tienen
    el mismo hash guardado — esto protege contra ataques que comparan
    hashes conocidos (rainbow tables).

    El resultado es irreversible: no existe una función para "deshacer"
    el hash y recuperar la contraseña original. Solo se puede comparar
    (ver verify_password).
    """
    # bcrypt trabaja con bytes, no con strings directamente — por eso
    # codificamos antes de hashear, y decodificamos el resultado para
    # poder guardarlo como texto normal en la base de datos.
    password_bytes = plain_password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Compara una contraseña en texto plano contra un hash ya guardado.

    No se "deshace" el hash para comparar — bcrypt vuelve a hashear la
    contraseña ingresada usando la misma sal que ya está codificada
    dentro del hash guardado, y compara los resultados.
    """
    password_bytes = plain_password.encode("utf-8")
    hashed_bytes = hashed_password.encode("utf-8")
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(user_id: int) -> str:
    """
    Genera un JWT (JSON Web Token) que representa una sesión iniciada.

    El token contiene:
    - "sub" (subject): el id del usuario — así, cuando llegue una
      petición con este token, sabemos de quién es sin consultar
      la base de datos cada vez solo para "saber quién eres".
    - "exp" (expiration): cuándo deja de ser válido — por seguridad,
      un token nunca debería durar para siempre.

    El token se "firma" con SECRET_KEY: cualquiera puede leer su
    contenido (los JWT no son secretos ni están encriptados), pero
    solo alguien que conozca SECRET_KEY puede generar un token que
    el servidor acepte como válido — eso es lo que evita que alguien
    se invente un token falso.
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),
        "exp": expire,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_access_token(token: str) -> int | None:
    """
    Verifica un token y, si es válido, devuelve el id del usuario.

    Devuelve None en dos casos distintos, tratados igual a propósito:
    - El token expiró (jwt.ExpiredSignatureError)
    - El token es inválido o fue manipulado (jwt.InvalidTokenError)

    No distinguimos esos dos casos en el valor de retorno porque, para
    quien usa la API, el resultado práctico es el mismo: el token no
    sirve y debe volver a iniciar sesión.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        return user_id
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None