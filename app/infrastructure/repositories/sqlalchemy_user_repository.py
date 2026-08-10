from sqlalchemy.orm import Session
from app.domain.repositories.user_repository import UserRepository
from app.domain.models.user import User
from app.infrastructure.orm_models.user_orm import UserORM


class SQLAlchemyUserRepository(UserRepository):
    """
    Implementación real del UserRepository, usando SQLAlchemy y Postgres.
    Mismo patrón que SQLAlchemyTaskRepository.
    """

    def __init__(self, db: Session):
        self.db = db

    def save(self, user: User) -> User:
        if user.id is None:
            user_orm = UserORM(
                email=user.email,
                full_name=user.full_name,
                hashed_password=user.hashed_password,
                is_active=user.is_active,
                created_at=user.created_at,
            )
            self.db.add(user_orm)
        else:
            user_orm = self.db.query(UserORM).filter(UserORM.id == user.id).first()
            if user_orm is None:
                raise ValueError(f"No existe un usuario con id {user.id}")
            user_orm.email = user.email
            user_orm.full_name = user.full_name
            user_orm.hashed_password = user.hashed_password
            user_orm.is_active = user.is_active

        self.db.commit()
        self.db.refresh(user_orm)
        return self._to_domain(user_orm)

    def get_by_id(self, user_id: int) -> User | None:
        user_orm = self.db.query(UserORM).filter(UserORM.id == user_id).first()
        return self._to_domain(user_orm) if user_orm else None

    def get_by_email(self, email: str) -> User | None:
        # A diferencia de la versión en memoria (que recorre todos los
        # usuarios uno por uno), aquí Postgres usa el índice que
        # definimos en UserORM.email — mucho más eficiente cuando la
        # tabla crece a miles de usuarios.
        user_orm = self.db.query(UserORM).filter(UserORM.email == email).first()
        return self._to_domain(user_orm) if user_orm else None

    def delete(self, user_id: int) -> bool:
        user_orm = self.db.query(UserORM).filter(UserORM.id == user_id).first()
        if user_orm is None:
            return False
        self.db.delete(user_orm)
        self.db.commit()
        return True

    def _to_domain(self, user_orm: UserORM) -> User:
        """Convierte un UserORM en un User de dominio (Pydantic)."""
        return User(
            id=user_orm.id,
            email=user_orm.email,
            full_name=user_orm.full_name,
            hashed_password=user_orm.hashed_password,
            is_active=user_orm.is_active,
            created_at=user_orm.created_at,
        )