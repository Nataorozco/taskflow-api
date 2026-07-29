from app.domain.agents.base_agent import BaseAgent
from app.domain.models.workflow_plan import WorkflowPlan, PlannedStep
from app.core.config import ANTHROPIC_API_KEY, LLM_MODEL


class WorkflowPlannerAgent(BaseAgent):
    """
    Convierte una meta en un plan de trabajo estructurado.
    Es el agente más complejo: en el futuro puede orquestar a los
    otros tres agentes (analizar cada paso, generar recordatorios, etc.)
    """

    name = "WorkflowPlannerAgent"

    def run(self, goal: str, owner_id: int) -> dict:
        try:
            self.log(f"Planificando meta: '{goal}'")

            if not ANTHROPIC_API_KEY:
                self.log("⚠️ No hay API key configurada, usando planificación simulada")
                plan = self._simulate_plan(goal, owner_id)
            else:
                plan = self._call_llm(goal, owner_id)

            self.log(f"✅ Plan generado con {len(plan.steps)} pasos")
            return {
                "success": True,
                "agent": self.name,
                "plan": plan
            }

        except Exception as e:
            return self.handle_error(e)

    def _simulate_plan(self, goal: str, owner_id: int) -> WorkflowPlan:
        """
        Planificación simulada, sin LLM. Genera pasos genéricos
        basados en una estructura estándar de proyecto.
        """
        generic_steps = [
            ("Investigar y definir el alcance", "Aclarar qué implica exactamente la meta antes de empezar."),
            ("Dividir en tareas concretas", "Convertir la meta general en pasos accionables."),
            ("Ejecutar la primera tarea", "Comenzar con el paso de mayor impacto o urgencia."),
            ("Revisar avance", "Evaluar qué se ha logrado y ajustar el plan si es necesario."),
            ("Finalizar y documentar", "Cerrar la meta y dejar registro de lo aprendido."),
        ]

        steps = [
            PlannedStep(
                order=i + 1,
                title=title,
                description=description,
                estimated_priority="high" if i == 0 else "medium"
            )
            for i, (title, description) in enumerate(generic_steps)
        ]

        return WorkflowPlan(goal=goal, steps=steps, owner_id=owner_id)

    def _call_llm(self, goal: str, owner_id: int) -> WorkflowPlan:
        """
        Punto de integración real con Claude.
        El prompt maestro para este agente se define por separado.
        """
        # TODO: implementar llamada real a la API de Anthropic
        raise NotImplementedError("Integración con LLM pendiente de implementar")