from app.domain.agents.base_agent import BaseAgent
from app.domain.models.task import Task, TaskPriority
from app.core.config import ANTHROPIC_API_KEY, LLM_MODEL


class TaskAnalyzerAgent(BaseAgent):
    """
    Analiza una tarea creada por el usuario y la enriquece:
    - Sugiere una prioridad si no es clara
    - Detecta si la descripción es ambigua o incompleta
    - Genera una versión mejorada de la descripción
    """

    name = "TaskAnalyzerAgent"

    def run(self, task: Task) -> dict:
        try:
            self.log(f"Analizando tarea: '{task.title}'")

            if not ANTHROPIC_API_KEY:
                self.log("⚠️ No hay API key configurada, usando análisis simulado")
                analysis = self._simulate_analysis(task)
            else:
                analysis = self._call_llm(task)

            self.log("✅ Análisis completado")
            return {
                "success": True,
                "agent": self.name,
                "task_id": task.id,
                "analysis": analysis
            }

        except Exception as e:
            return self.handle_error(e)

    def _simulate_analysis(self, task: Task) -> dict:
        """
        Análisis simulado, sin LLM. Sirve para desarrollar y probar
        el resto del pipeline mientras se define la integración real.
        """
        suggested_priority = TaskPriority.HIGH if len(task.title) < 20 else TaskPriority.MEDIUM
        is_ambiguous = task.description is None or len(task.description.strip()) < 10

        return {
            "suggested_priority": suggested_priority,
            "is_ambiguous": is_ambiguous,
            "improved_description": task.description or "Sin descripción — se recomienda agregar más contexto.",
            "source": "simulated"
        }

    def _call_llm(self, task: Task) -> dict:
        """
        Punto de integración real con Claude.
        Cuando se conecte la API, esta función reemplaza a _simulate_analysis
        sin que el resto del agente necesite cambiar.
        """
        # TODO: implementar llamada real a la API de Anthropic
        # usando ANTHROPIC_API_KEY y LLM_MODEL
        raise NotImplementedError("Integración con LLM pendiente de implementar")