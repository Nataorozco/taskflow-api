from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    Crea una sesión de base de datos y la cierra automáticamente al terminar.
    Se usa como 'context manager' o inyectada en endpoints de FastAPI más adelante.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()