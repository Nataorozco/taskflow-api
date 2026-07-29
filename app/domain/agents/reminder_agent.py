from datetime import datetime, timedelta, timezone
from app.domain.agents.base_agent import BaseAgent
from app.domain.models.task import Task, TaskPriority
from app.core.config import ANTHROPIC_API_KEY, LLM_MODEL


class ReminderAgent(BaseAgent):
    """
    Genera recordatorios inteligentes para una tarea, basándose en:
    - Su fecha límite (due_date)
    - Su prioridad
    - Cuánto tiempo falta para el vencimiento
    """

    name = "ReminderAgent"

    def run(self, task: Task) -> dict:
        try:
            self.log(f"Generando recordatorio para: '{task.title}'")

            if not ANTHROPIC_API_KEY:
                self.log("⚠️ No hay API key configurada, usando lógica simulada")
                reminder = self._simulate_reminder(task)
            else:
                reminder = self._call_llm(task)

            self.log("✅ Recordatorio generado")
            return {
                "success": True,
                "agent": self.name,
                "task_id": task.id,
                "reminder": reminder
            }

        except Exception as e:
            return self.handle_error(e)

    def _simulate_reminder(self, task: Task) -> dict:
        """
        Lógica simulada, sin LLM. Calcula un recordatorio basado en
        reglas simples de fecha y prioridad.
        """
        if task.due_date is None:
            return {
                "should_remind": False,
                "message": "Esta tarea no tiene fecha límite definida.",
                "source": "simulated"
            }

        now = datetime.now(timezone.utc)
        time_left = task.due_date - now

        # Cuánto antes recordar, según la prioridad
        buffer_by_priority = {
            TaskPriority.HIGH: timedelta(days=2),
            TaskPriority.MEDIUM: timedelta(days=1),
            TaskPriority.LOW: timedelta(hours=6),
        }
        buffer = buffer_by_priority.get(task.priority, timedelta(days=1))

        should_remind = time_left <= buffer and time_left.total_seconds() > 0
        is_overdue = time_left.total_seconds() < 0

        if is_overdue:
            message = f"⚠️ La tarea '{task.title}' está vencida."
        elif should_remind:
            message = f"🔔 La tarea '{task.title}' vence pronto ({task.due_date.strftime('%d/%m/%Y %H:%M')})."
        else:
            message = f"La tarea '{task.title}' aún no requiere recordatorio."

        return {
            "should_remind": should_remind or is_overdue,
            "is_overdue": is_overdue,
            "message": message,
            "source": "simulated"
        }

    def _call_llm(self, task: Task) -> dict:
        """
        Punto de integración real con Claude.
        El prompt maestro para este agente se define por separado.
        """
        # TODO: implementar llamada real a la API de Anthropic
        raise NotImplementedError("Integración con LLM pendiente de implementar")