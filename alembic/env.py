from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy import create_engine
from alembic import context

from app.infrastructure.database import Base
# Cada modelo ORM se importa aquí para que Alembic pueda "verlo" al
# comparar el estado de los modelos contra la base de datos real.
# Si se agrega un modelo ORM nuevo en el futuro, debe importarse
# también aquí, o Alembic no lo detectará al generar migraciones.
from app.infrastructure.orm_models.task_orm import TaskORM
from app.infrastructure.orm_models.user_orm import UserORM
from app.infrastructure.orm_models.document_orm import DocumentORM
from app.core.config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# target_metadata le dice a Alembic dónde están definidos todos los
# modelos ORM — Base.metadata reúne automáticamente TaskORM, UserORM
# y DocumentORM en cuanto se importan arriba.
target_metadata = Base.metadata

# Construimos la URL de conexión desde .env, igual que en database.py
# — nunca se deja una URL con contraseña escrita directamente en
# alembic.ini (esa línea quedó comentada intencionalmente ahí).
DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


def run_migrations_offline() -> None:
    """
    Modo 'offline': genera el SQL de la migración como texto, sin
    necesitar una conexión real a la base de datos. Útil para revisar
    qué SQL se ejecutaría antes de aplicarlo, o generar scripts para
    ejecutar manualmente en otro entorno.
    """
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Modo 'online': se conecta de verdad a Postgres y aplica la
    migración directamente. Es el modo que se usa en el día a día
    (alembic upgrade head).
    """
    connectable = create_engine(DATABASE_URL, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
