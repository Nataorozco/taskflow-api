# taskflow-api

Backend API para gestionar usuarios, tareas, documentos y automatizaciones 
inteligentes mediante agentes de IA.

## 🎯 Sobre el proyecto

TaskFlow es una API construida con FastAPI que combina gestión de tareas 
tradicional con un pipeline de agentes de IA capaces de analizar tareas, 
resumir documentos, generar recordatorios inteligentes y planificar flujos 
de trabajo a partir de una meta.

## 🏗️ Arquitectura

- Clean Architecture + Service Layer
- Diseñado para integrar modelos de IA (OpenAI, Claude)
- Preparado para evolucionar hacia microservicios

## 🛠️ Stack tecnológico

- **Backend:** FastAPI, Python 3.14
- **Base de datos:** PostgreSQL 18, SQLAlchemy
- **Validación:** Pydantic
- **Entorno:** WSL2 (Ubuntu), Docker (planeado)

## 📌 Estado actual

🚧 En desarrollo activo — MVP en construcción.

- [x] Conexión segura a base de datos (variables de entorno)
- [x] Modelos de dominio (Task, User, Document)
- [ ] Interfaz base para agentes de IA
- [ ] Cuatro agentes: TaskAnalyzer, DocumentSummarizer, Reminder, WorkflowPlanner
- [ ] Endpoints CRUD
- [ ] Autenticación
- [ ] Tests

## 👩‍💻 Autora

Nataly Orozco 