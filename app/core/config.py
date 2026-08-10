import os
from dotenv import load_dotenv

# load_dotenv() lee el archivo .env (que nunca se sube a git, ver
# .gitignore) y carga sus valores como variables de entorno del
# sistema, disponibles a través de os.getenv().
load_dotenv()

# Variables de conexión a Postgres. Los valores reales viven solo en
# .env — este archivo nunca contiene contraseñas escritas directamente,
# solo sabe CÓMO leerlas.
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_PORT = os.getenv("DB_PORT", "5432")

# Configuración para la futura integración con Claude. ANTHROPIC_API_KEY
# empieza vacía a propósito (default=""), lo que le permite a cada
# agente decidir automáticamente si usar lógica simulada o real: ver
# el patrón "if not ANTHROPIC_API_KEY" en cada uno de los 4 agentes.
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "claude-sonnet-4-6")