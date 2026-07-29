from datetime import datetime, timedelta, timezone
from app.domain.agents.reminder_agent import ReminderAgent
from app.domain.models.task import Task, TaskPriority

# Caso 1: tarea que vence pronto
task_urgente = Task(
    title="Entregar informe",
    owner_id=1,
    priority=TaskPriority.HIGH,
    due_date=datetime.now(timezone.utc) + timedelta(hours=5)
)

# Caso 2: tarea sin fecha límite
task_sin_fecha = Task(
    title="Organizar escritorio",
    owner_id=1
)

agent = ReminderAgent()

print("--- Caso 1: tarea urgente ---")
print(agent.run(task_urgente))
print()
print("--- Caso 2: sin fecha límite ---")
print(agent.run(task_sin_fecha))