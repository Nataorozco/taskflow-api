from abc import ABC, abstractmethod
from app.domain.models.user import User


class UserRepository(ABC):
    """
    Contrato abstracto para persistir y consultar usuarios.
    """

    @abstractmethod
    def save(self, user: User) -> User:
        """Crea o actualiza un usuario. Devuelve el usuario guardado (con id asignado)."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None:
        """Busca un usuario por su id. Devuelve None si no existe."""
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        """Busca un usuario por su email. Útil para login. Devuelve None si no existe."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Elimina un usuario. Devuelve True si se eliminó, False si no existía."""
        raise NotImplementedError