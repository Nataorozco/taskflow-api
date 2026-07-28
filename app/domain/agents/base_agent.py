from abc import ABC, abstractmethod
from typing import Any


class BaseAgent(ABC):
    """
    Contrato base que deben seguir todos los agentes de TaskFlow.
    Cada agente recibe un input, lo procesa, y devuelve un output —
    con manejo de errores y logging consistente entre todos.
    """

    name: str = "BaseAgent"

    @abstractmethod
    def run(self, input_data: Any) -> Any:
        """
        Ejecuta la lógica principal del agente.
        Cada agente concreto debe implementar este método.
        """
        raise NotImplementedError

    def log(self, message: str) -> None:
        """Logging simple y consistente para todos los agentes."""
        print(f"[{self.name}] {message}")

    def handle_error(self, error: Exception) -> dict:
        """Manejo de errores consistente entre todos los agentes."""
        self.log(f"❌ Error: {error}")
        return {
            "success": False,
            "agent": self.name,
            "error": str(error)
        }