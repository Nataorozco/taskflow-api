from app.domain.repositories.user_repository import UserRepository
from app.domain.models.user import User


class InMemoryUserRepository(UserRepository):
    """
    Implementación en memoria del UserRepository.
    Mismo principio que InMemoryTaskRepository.
    """

    def __init__(self):
        self._users: dict[int, User] = {}
        self._next_id = 1

    def save(self, user: User) -> User:
        if user.id is None:
            user.id = self._next_id
            self._next_id += 1
        self._users[user.id] = user
        return user

    def get_by_id(self, user_id: int) -> User | None:
        return self._users.get(user_id)

    def get_by_email(self, email: str) -> User | None:
        # Como no hay índice real (esto es solo un diccionario en
        # memoria), buscar por email requiere recorrer todos los
        # usuarios uno por uno. En la versión real con SQLAlchemy,
        # esto es mucho más eficiente gracias al índice de la columna.
        for user in self._users.values():
            if user.email == email:
                return user
        return None

    def delete(self, user_id: int) -> bool:
        if user_id in self._users:
            del self._users[user_id]
            return True
        return False