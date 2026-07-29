from app.domain.agents.workflow_planner_agent import WorkflowPlannerAgent

agent = WorkflowPlannerAgent()
resultado = agent.run(
    goal="Lanzar mi portafolio de desarrolladora antes de noviembre",
    owner_id=1
)
print()
print("Resultado:", resultado)