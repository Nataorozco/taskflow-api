from app.domain.agents.document_summarizer_agent import DocumentSummarizerAgent
from app.domain.models.document import Document, DocumentType

document = Document(
    title="Guía de Clean Architecture",
    content=(
        "Clean Architecture es un enfoque de diseño de software que separa "
        "las responsabilidades en capas independientes. El objetivo principal "
        "es que la lógica de negocio no dependa de frameworks, bases de datos "
        "ni interfaces externas. Esto permite que el sistema sea más testeable, "
        "mantenible y flexible ante cambios tecnológicos futuros."
    ),
    doc_type=DocumentType.MARKDOWN,
    owner_id=1
)

agent = DocumentSummarizerAgent()
resultado = agent.run(document)
print()
print("Resultado:", resultado)