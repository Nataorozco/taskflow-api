from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone
from app.infrastructure.database import Base


class UserORM(Base):
    """
    Modelo ORM de un usuario — representa la tabla 'users' en Postgres.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    # unique=True: regla de la BASE DE DATOS (no solo del código en
    # Python) que impide que existan dos usuarios con el mismo email,
    # incluso si algún día hay un bug en la validación de la aplicación.
    # index=True: acelera las búsquedas por email (get_by_email, login).
    email = Column(String, nullable=False, unique=True, index=True)

    full_name = Column(String, nullable=False)

    # Solo se guarda el HASH de la contraseña, nunca la contraseña real.
    hashed_password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))