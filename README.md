# TaskFlow API

Backend API para gestionar usuarios, tareas, documentos y automatizaciones 
inteligentes mediante agentes de IA.

## 🎯 Sobre el proyecto

TaskFlow es una API construida con FastAPI que combina gestión de tareas 
tradicional con un pipeline de agentes de IA capaces de analizar tareas, 
resumir documentos, generar recordatorios inteligentes y planificar flujos 
de trabajo a partir de una meta.

## 💡 ¿Por qué importa?

La mayoría de herramientas de gestión de tareas solo almacenan datos — el usuario sigue haciendo todo el trabajo de pensar: priorizar, resumir, recordar, planificar. TaskFlow va un paso más allá: integra agentes de IA directamente en el flujo de trabajo para automatizar ese esfuerzo mental.

**Beneficios concretos:**
- ⏱️ **Ahorra tiempo real** — en vez de leer un documento completo, `DocumentSummarizerAgent` entrega el resumen y los puntos clave en segundos.
- 🎯 **Reduce tareas olvidadas o mal priorizadas** — `TaskAnalyzerAgent` y `ReminderAgent` automatizan juicios que normalmente dependen de que una persona esté atenta todo el día.
- 🗺️ **Acelera la planificación** — `WorkflowPlannerAgent` convierte una meta ambigua ("lanzar mi producto antes de diciembre") en una lista de pasos concretos, sin partir de una hoja en blanco.
- 🔌 **Es una API, no una app cerrada** — cualquier empresa puede integrar estas capacidades dentro de su propio sistema (su CRM, su herramienta interna, su producto), en vez de depender de una herramienta externa de terceros.

**Casos de uso:**
- Equipos pequeños que necesitan gestión de tareas con automatización, sin pagar por herramientas enterprise complejas.
- Empresas que quieren agregar capacidades de IA a su propio software interno, consumiendo esta API en vez de construir agentes desde cero.
- Uso personal: automatizar la gestión de tareas y proyectos propios.

## 🏗️ Arquitectura

- Clean Architecture + Service Layer + Repository Pattern
- Capa de dominio 100% independiente de frameworks externos (Pydantic puro)
- Diseñado para integrar modelos de IA (Claude)
- Preparado para evolucionar hacia microservicios

## 🛠️ Stack tecnológico

- **Backend:** FastAPI, Python 3.14
- **Base de datos:** PostgreSQL 18, SQLAlchemy 2.0, Alembic (migraciones versionadas)
- **Validación:** Pydantic
- **Entorno:** Ubuntu (dual-boot / WSL2), entorno virtual (.venv)

## 📌 Estado actual

🚧 En desarrollo activo — MVP en construcción.

**Completo:**
- [x] Conexión segura a base de datos (variables de entorno, nunca credenciales en código)
- [x] Modelos de dominio (Task, User, Document, WorkflowPlan)
- [x] Interfaz base para agentes de IA (BaseAgent)
- [x] Cuatro agentes con lógica simulada funcionando: TaskAnalyzerAgent, 
      DocumentSummarizerAgent, ReminderAgent, WorkflowPlannerAgent
- [x] Repositorios abstractos + implementación en memoria + implementación 
      real con SQLAlchemy para Task, User y Document
- [x] Migraciones de base de datos con Alembic (tablas tasks, users, documents)
- [x] Endpoints CRUD de Task (crear, obtener, listar, eliminar) con FastAPI
- [x] Documentación automática interactiva (/docs)
- [x] Código completamente comentado, explicando el porqué de cada decisión

**Pendiente:**
- [ ] Endpoints CRUD de User y Document
- [ ] Autenticación (login, JWT)
- [ ] Integración real con Claude (prompts maestros + implementación de 
      _call_llm() en cada agente)
- [ ] Redis (caché y rate limiting)
- [ ] Docker
- [ ] Tests automatizados con pytest
- [ ] Documentación final y ejemplos de uso

## 👩‍💻 Autora

Nataly Orozco NOrionDev— Estudiante de Ingeniería, Universidad de Antioquia