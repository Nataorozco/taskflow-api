from app.domain.models.task import Task, TaskStatus, TaskPriority
from app.domain.models.user import User
from app.domain.models.document import Document, DocumentType

# Probando el modelo User
user = User(
    email="natalia@example.com",
    full_name="Natalia Orozco",
    hashed_password="hash_de_ejemplo_no_real"
)
print("✅ User creado:")
print(user)
print()

# Probando el modelo Task
task = Task(
    title="Terminar el modelo de dominio",
    description="Definir Task, User y Document con Pydantic",
    priority=TaskPriority.HIGH,
    owner_id=1
)
print("✅ Task creada:")
print(task)
print()

# Probando el modelo Document
document = Document(
    title="Especificación del proyecto",
    content="Este documento describe la arquitectura de TaskFlow API...",
    doc_type=DocumentType.MARKDOWN,
    owner_id=1
)
print("✅ Document creado:")
print(document)