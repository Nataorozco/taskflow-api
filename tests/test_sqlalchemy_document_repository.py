from app.infrastructure.database import SessionLocal
from app.infrastructure.repositories.sqlalchemy_document_repository import SQLAlchemyDocumentRepository
from app.domain.models.document import Document, DocumentType

db = SessionLocal()
repo = SQLAlchemyDocumentRepository(db)

document = repo.save(Document(
    title="Documento de prueba real",
    content="Confirmando que se guarda en Postgres de verdad.",
    doc_type=DocumentType.MARKDOWN,
    owner_id=1
))
print("--- Guardado ---")
print(document)

print()
print("--- Buscar por owner 1 ---")
print(repo.get_all_by_owner(1))

db.close()