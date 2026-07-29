from app.domain.agents.task_analyzer_agent import TaskAnalyzerAgent
from app.domain.models.task import Task

task = Task(
    title="Reunión",
    description="",
    owner_id=1
)

agent = TaskAnalyzerAgent()
resultado = agent.run(task)
print()
print("Resultado:", resultado)