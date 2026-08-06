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

            # Decisión de diseño clave: si no hay API key configurada,
            # usamos análisis simulado en vez de fallar. Esto permite
            # desarrollar y probar todo el pipeline del agente sin
            # depender de tener una cuenta de Claude activa todavía.
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
        Análisis simulado, sin LLM. Usa reglas simples de Python en vez
        de inteligencia artificial real, para poder desarrollar y probar
        el resto del pipeline mientras se define la integración real
        con Claude (los prompts se van a diseñar por separado, con ChatGPT).
        """
        # Regla simple: títulos cortos se asumen más urgentes/directos.
        suggested_priority = TaskPriority.HIGH if len(task.title) < 20 else TaskPriority.MEDIUM

        # Una tarea se considera "ambigua" si no tiene descripción,
        # o si la descripción es demasiado corta para ser útil.
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

        Diseño intencional: run() nunca cambia, sin importar si se usa
        _simulate_analysis() o _call_llm() — solo decide cuál llamar según
        si hay API key. Cuando se implemente esta función, el agente
        completo empieza a funcionar con IA real, sin tocar nada más.
        """
        # TODO: implementar llamada real a la API de Anthropic
        # usando ANTHROPIC_API_KEY y LLM_MODEL
        raise NotImplementedError("Integración con LLM pendiente de implementar")