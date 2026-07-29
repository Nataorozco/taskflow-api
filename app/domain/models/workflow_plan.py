from pydantic import BaseModel, Field
from datetime import datetime, timezone


class PlannedStep(BaseModel):
    """Un paso individual dentro de un plan de trabajo."""
    order: int
    title: str
    description: str | None = None
    estimated_priority: str = "medium"


class WorkflowPlan(BaseModel):
    """
    Plan de trabajo generado a partir de una meta.
    Cada paso puede convertirse después en una Task real.
    """
    id: int | None = None
    goal: str
    steps: list[PlannedStep] = []
    owner_id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))