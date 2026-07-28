from app.domain.agents.base_agent import BaseAgent


class EchoAgent(BaseAgent):
    """Agente de prueba: solo repite el input, para validar que BaseAgent funciona."""

    name = "EchoAgent"

    def run(self, input_data):
        try:
            self.log(f"Procesando input: {input_data}")
            result = {
                "success": True,
                "agent": self.name,
                "output": input_data
            }
            self.log("✅ Procesado correctamente")
            return result
        except Exception as e:
            return self.handle_error(e)


# Prueba
agent = EchoAgent()
resultado = agent.run("Hola, este es un mensaje de prueba")
print()
print("Resultado final:", resultado)