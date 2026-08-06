from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """
    Contrato base que deben seguir todos los agentes de TaskFlow.

    ABC (Abstract Base Class) + @abstractmethod obligan a que cualquier
    clase que herede de BaseAgent implemente su propio método run() —
    si no lo hace, Python da error al intentar crear ese agente. Así
    garantizamos que los 4 agentes (TaskAnalyzer, DocumentSummarizer,
    Reminder, WorkflowPlanner) tengan la misma forma por fuera, aunque
    hagan cosas completamente distintas por dentro.
    """

    # Cada agente concreto sobrescribe esto con su propio nombre
    # (ej. "TaskAnalyzerAgent"), para que el logging identifique
    # claramente quién está hablando.
    name: str = "BaseAgent"

    @abstractmethod
    def run(self, input_data: Any) -> Any:
        """
        Ejecuta la lógica principal del agente.
        Cada agente concreto debe implementar este método —
        es el único método que Python exige por el @abstractmethod.
        """
        raise NotImplementedError

    def log(self, message: str) -> None:
        """
        Logging simple y consistente para todos los agentes.
        Al centralizarlo aquí, evitamos repetir la misma lógica de
        impresión en cada uno de los 4 agentes.
        """
        print(f"[{self.name}] {message}")

    def handle_error(self, error: Exception) -> dict:
        """
        Manejo de errores consistente entre todos los agentes.
        Devuelve siempre la misma forma de diccionario (success, agent,
        error), para que el código que llama a cualquier agente pueda
        manejar los fallos de manera uniforme, sin importar cuál agente
        fue el que falló.
        """
        self.log(f"❌ Error: {error}")
        return {
            "success": False,
            "agent": self.name,
            "error": str(error)
        }