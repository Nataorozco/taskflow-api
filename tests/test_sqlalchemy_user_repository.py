from app.infrastructure.database import SessionLocal
from app.infrastructure.repositories.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.domain.models.user import User
import uuid

db = SessionLocal()
repo = SQLAlchemyUserRepository(db)

# Usamos un email único en cada corrida (con un fragmento aleatorio),
# para evitar chocar con la restricción unique=True de la columna
# email si el test ya se corrió antes.
unique_email = f"natalia.test.{uuid.uuid4().hex[:8]}@example.com"

user = repo.save(User(
    email=unique_email,
    full_name="Natalia Orozco",
    hashed_password="hash_de_prueba"
))
print("--- Guardado ---")
print(user)

print()
print("--- Buscar por email ---")
print(repo.get_by_email(unique_email))

db.close()