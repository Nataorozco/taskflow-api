from fastapi import FastAPI
from app.api.routers import task_router

# FastAPI() crea la aplicación en sí. title y description aparecen
# automáticamente en la documentación interactiva que FastAPI genera
# solo (accesible en /docs una vez el servidor esté corriendo).
app = FastAPI(
    title="TaskFlow API",
    description="Backend API para gestionar usuarios, tareas, documentos y automatizaciones inteligentes mediante agentes de IA.",
    version="0.1.0",
)

# include_router "monta" todos los endpoints definidos en task_router.py
# dentro de la aplicación principal. Como task_router ya tiene
# prefix="/tasks" definido en sí mismo, las rutas finales quedan como
# /tasks, /tasks/{task_id}, etc. — sin repetir el prefijo aquí.
app.include_router(task_router.router)


@app.get("/")
def read_root():
    """
    Endpoint raíz, simple, solo para confirmar que la API está viva.
    Útil como primer punto de prueba al levantar el servidor.
    """
    return {"message": "TaskFlow API está funcionando 🚀"}