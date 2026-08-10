from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

# Construimos la URL de conexión a partir de las variables de .env,
# nunca escribiendo la contraseña directamente aquí. postgresql+psycopg
# le dice a SQLAlchemy qué "dialecto" y driver usar para hablar con Postgres.
DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# El Engine es la conexión "maestra" a la base de datos. Se crea una
# sola vez cuando arranca la aplicación, y todo lo demás se apoya en él.
# echo=False evita que SQLAlchemy imprima cada consulta SQL en consola
# (útil ponerlo en True temporalmente si algún día se necesita depurar).
engine = create_engine(DATABASE_URL, echo=False)

# sessionmaker no crea una sesión todavía — crea una "fábrica" de
# sesiones. Cada vez que se llama a SessionLocal(), se obtiene una
# sesión nueva e independiente.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base es la clase especial de la que heredan todos los modelos ORM
# (TaskORM, UserORM, DocumentORM). Es diferente de BaseModel de
# Pydantic — cumplen roles distintos y no deben confundirse.
Base = declarative_base()


def get_db():
    """
    Crea una sesión de base de datos y la cierra automáticamente al
    terminar de usarla.

    El uso de 'yield' en vez de 'return' es un patrón de Python para
    "entregar algo, dejar que se use, y luego limpiar" — abre la
    sesión, la entrega a quien la necesite, y el bloque 'finally'
    garantiza que se cierre correctamente incluso si ocurre un error
    mientras se usa. Este patrón se conecta directamente con FastAPI
    más adelante (Depends(get_db) en los endpoints).
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()