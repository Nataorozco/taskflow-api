from sqlalchemy.orm import Session
from app.domain.repositories.document_repository import DocumentRepository
from app.domain.models.document import Document
from app.infrastructure.orm_models.document_orm import DocumentORM


class SQLAlchemyDocumentRepository(DocumentRepository):
    """
    Implementación real del DocumentRepository, usando SQLAlchemy y Postgres.
    """

    def __init__(self, db: Session):
        self.db = db

    def save(self, document: Document) -> Document:
        if document.id is None:
            document_orm = DocumentORM(
                title=document.title,
                content=document.content,
                doc_type=document.doc_type,
                task_id=document.task_id,
                owner_id=document.owner_id,
                summary=document.summary,
                created_at=document.created_at,
            )
            self.db.add(document_orm)
        else:
            document_orm = self.db.query(DocumentORM).filter(DocumentORM.id == document.id).first()
            if document_orm is None:
                raise ValueError(f"No existe un documento con id {document.id}")
            document_orm.title = document.title
            document_orm.content = document.content
            document_orm.doc_type = document.doc_type
            document_orm.task_id = document.task_id
            document_orm.summary = document.summary

        self.db.commit()
        self.db.refresh(document_orm)
        return self._to_domain(document_orm)

    def get_by_id(self, document_id: int) -> Document | None:
        document_orm = self.db.query(DocumentORM).filter(DocumentORM.id == document_id).first()
        return self._to_domain(document_orm) if document_orm else None

    def get_all_by_owner(self, owner_id: int) -> list[Document]:
        docs_orm = self.db.query(DocumentORM).filter(DocumentORM.owner_id == owner_id).all()
        return [self._to_domain(d) for d in docs_orm]

    def get_all_by_task(self, task_id: int) -> list[Document]:
        docs_orm = self.db.query(DocumentORM).filter(DocumentORM.task_id == task_id).all()
        return [self._to_domain(d) for d in docs_orm]

    def delete(self, document_id: int) -> bool:
        document_orm = self.db.query(DocumentORM).filter(DocumentORM.id == document_id).first()
        if document_orm is None:
            return False
        self.db.delete(document_orm)
        self.db.commit()
        return True

    def _to_domain(self, document_orm: DocumentORM) -> Document:
        return Document(
            id=document_orm.id,
            title=document_orm.title,
            content=document_orm.content,
            doc_type=document_orm.doc_type,
            task_id=document_orm.task_id,
            owner_id=document_orm.owner_id,
            summary=document_orm.summary,
            created_at=document_orm.created_at,
        )