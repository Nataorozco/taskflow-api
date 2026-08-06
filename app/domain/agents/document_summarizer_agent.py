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
        Resumen simulado, sin LLM. Estas reglas son deliberadamente
        simples (no intentan "entender" el texto) — su único propósito
        es dar una salida con la MISMA FORMA que va a tener la respuesta
        real del LLM, para poder construir y probar el resto del sistema
        (endpoints, guardado en base de datos, etc.) sin esperar a tener
        la integración con Claude lista.
        """
        words = document.content.split()
        word_count = len(words)

        # Estimación estándar de velocidad de lectura: ~200 palabras
        # por minuto es un promedio ampliamente usado como referencia.
        reading_time_minutes = max(1, round(word_count / 200))

        # Resumen simulado: simplemente las primeras ~30 palabras.
        # Un LLM real generaría un resumen genuino, no un recorte.
        preview = " ".join(words[:30])
        simulated_summary = f"{preview}..." if word_count > 30 else preview

        # Palabras clave simuladas: aproximación muy básica usando
        # las 5 palabras más largas del texto (sin repetir). Un LLM
        # real identificaría conceptos importantes, no solo longitud.
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
        El prompt maestro para este agente se define por separado
        (con ChatGPT, según el flujo de trabajo definido para el
        proyecto).
        """
        # TODO: implementar llamada real a la API de Anthropic
        raise NotImplementedError("Integración con LLM pendiente de implementar")