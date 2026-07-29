from app.domain.agents.base_agent import BaseAgent
from app.domain.models.document import Document
from app.core.config import ANTHROPIC_API_KEY, LLM_MODEL


class DocumentSummarizerAgent(BaseAgent):
    """
    Resume documentos y extrae información útil:
    - Genera un resumen breve del contenido
    - Extrae palabras clave
    - Estima el tiempo de lectura
    """

    name = "DocumentSummarizerAgent"

    def run(self, document: Document) -> dict:
        try:
            self.log(f"Resumiendo documento: '{document.title}'")

            if not ANTHROPIC_API_KEY:
                self.log("⚠️ No hay API key configurada, usando resumen simulado")
                summary_data = self._simulate_summary(document)
            else:
                summary_data = self._call_llm(document)

            self.log("✅ Resumen generado")
            return {
                "success": True,
                "agent": self.name,
                "document_id": document.id,
                "summary_data": summary_data
            }

        except Exception as e:
            return self.handle_error(e)

    def _simulate_summary(self, document: Document) -> dict:
        """
        Resumen simulado, sin LLM. Usa reglas simples sobre el texto
        para dar una idea aproximada del contenido.
        """
        words = document.content.split()
        word_count = len(words)

        # Estimación de tiempo de lectura: ~200 palabras por minuto
        reading_time_minutes = max(1, round(word_count / 200))

        # Resumen simulado: primeras ~30 palabras del contenido
        preview = " ".join(words[:30])
        simulated_summary = f"{preview}..." if word_count > 30 else preview

        # Palabras clave simuladas: las 5 palabras más largas (aproximación simple)
        keywords = sorted(set(words), key=len, reverse=True)[:5]

        return {
            "summary": simulated_summary,
            "keywords": keywords,
            "word_count": word_count,
            "estimated_reading_time_minutes": reading_time_minutes,
            "source": "simulated"
        }

    def _call_llm(self, document: Document) -> dict:
        """
        Punto de integración real con Claude.
        El prompt maestro para este agente se define por separado.
        """
        # TODO: implementar llamada real a la API de Anthropic
        raise NotImplementedError("Integración con LLM pendiente de implementar")