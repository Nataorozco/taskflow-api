from app.infrastructure.database import SessionLocal
from app.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.domain.models.user import User

db = SessionLocal()
repo = SQLAlchemyUserRepository(db)

user = repo.save(User(
    email="natalia.test@example.com",
    full_name="Natalia Orozco",
    hashed_password="hash_de_prueba"
))
print("--- Guardado ---")
print(user)

print()
print("--- Buscar por email ---")
print(repo.get_by_email("natalia.test@example.com"))

db.close()