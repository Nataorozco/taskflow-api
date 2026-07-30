from app.infrastructure.repositories.in_memory_user_repository import InMemoryUserRepository
from app.domain.models.user import User

repo = InMemoryUserRepository()

# Crear
user1 = repo.save(User(email="natalia@example.com", full_name="Natalia Orozco", hashed_password="hash1"))
user2 = repo.save(User(email="otro@example.com", full_name="Otro Usuario", hashed_password="hash2"))

print("--- Guardados ---")
print(user1)
print(user2)

print()
print("--- Buscar por id ---")
print(repo.get_by_id(1))

print()
print("--- Buscar por email ---")
print(repo.get_by_email("natalia@example.com"))
print("Email que no existe:", repo.get_by_email("noexiste@example.com"))

print()
print("--- Eliminar usuario 1 ---")
print("Eliminado:", repo.delete(1))
print("Buscar de nuevo:", repo.get_by_id(1))