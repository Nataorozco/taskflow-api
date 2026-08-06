from app.domain.agents.base_agent import BaseAgent
from app.domain.models.workflow_plan import WorkflowPlan, PlannedStep
from app.core.config import ANTHROPIC_API_KEY, LLM_MODEL


class WorkflowPlannerAgent(BaseAgent):
    """
    Convierte una meta en un plan de trabajo estructurado.

    Es el agente más complejo de los cuatro: a diferencia de los otros
    tres (que analizan algo que ya existe), este CREA algo nuevo a partir
    de una idea en texto libre. En el futuro puede orquestar a los otros
    tres agentes — por ejemplo, un plan que incluya crear tareas ya
    analizadas por TaskAnalyzerAgent y con recordatorios de ReminderAgent.
    """

    name = "WorkflowPlannerAgent"

    def run(self, goal: str, owner_id: int) -> dict:
        """
        Nota de diseño: run() recibe (goal: str, owner_id: int) en vez
        de un objeto de dominio como los otros agentes (que reciben
        Task o Document). Es intencional: este agente no analiza algo
        existente, sino que construye un WorkflowPlan desde cero.
        """
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
        Planificación simulada, sin LLM. Usa una estructura genérica de
        5 pasos que aplica razonablemente bien a cualquier meta general
        (investigar, dividir, ejecutar, revisar, cerrar) — no está
        adaptada al contenido específico de la meta todavía; eso es
        justamente lo que el LLM real va a aportar cuando se conecte.
        """
        generic_steps = [
            ("Investigar y definir el alcance", "Aclarar qué implica exactamente la meta antes de empezar."),
            ("Dividir en tareas concretas", "Convertir la meta general en pasos accionables."),
            ("Ejecutar la primera tarea", "Comenzar con el paso de mayor impacto o urgencia."),
            ("Revisar avance", "Evaluar qué se ha logrado y ajustar el plan si es necesario."),
            ("Finalizar y documentar", "Cerrar la meta y dejar registro de lo aprendido."),
        ]

        # El primer paso siempre se marca como alta prioridad (es el
        # punto de partida obligatorio); el resto queda en prioridad
        # media por defecto.
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