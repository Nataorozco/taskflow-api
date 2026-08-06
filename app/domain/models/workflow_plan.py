from pydantic import BaseModel, Field
from datetime import datetime, timezone


class PlannedStep(BaseModel):
    """
    Un paso individual dentro de un plan de trabajo generado por
    WorkflowPlannerAgent. No es una Task todavía — es una propuesta
    de tarea, pensada para poder convertirse en una Task real más
    adelante (por ejemplo, cuando el usuario apruebe el plan).
    """
    order: int
    title: str
    description: str | None = None

    # Texto libre por ahora ("high", "medium", "low") en vez de reutilizar
    # el Enum TaskPriority, porque este valor lo genera el LLM (o la
    # lógica simulada) y no siempre coincidirá exactamente con el Enum
    # hasta que se convierta formalmente en una Task.
    estimated_priority: str = "medium"


class WorkflowPlan(BaseModel):
    """
    Plan de trabajo generado a partir de una meta (goal) escrita por
    el usuario. Es el resultado del WorkflowPlannerAgent, el más
    complejo de los cuatro agentes: en el futuro puede orquestar a
    los otros tres (analizar cada paso, generar recordatorios, etc.).
    """

    id: int | None = None

    # La meta original tal como la escribió el usuario, sin modificar.
    # Se conserva para poder mostrarla junto al plan generado.
    goal: str

    # Lista de pasos generados; empieza vacía si el plan aún no se
    # ha generado (aunque en la práctica siempre se crea con pasos).
    steps: list[PlannedStep] = []

    owner_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))