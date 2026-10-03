from fastapi import FastAPI
from app.api.routers import task_router, user_router, document_router, auth_router

# FastAPI() crea la aplicación en sí. title y description aparecen
# automáticamente en la documentación interactiva que FastAPI genera
# solo (accesible en /docs una vez el servidor esté corriendo).
app = FastAPI(
    title="TaskFlow API",
    description="Backend API para gestionar usuarios, tareas, documentos y automatizaciones inteligentes mediante agentes de IA.",
    version="0.1.0",
)

# include_router "monta" todos los endpoints definidos en cada router
# dentro de la aplicación principal. Como cada router ya tiene su
# propio prefix (/tasks, /users, /documents, /auth) definido en sí
# mismo, las rutas finales quedan completas sin repetir el prefijo aquí.
app.include_router(task_router.router)
app.include_router(user_router.router)
app.include_router(document_router.router)
app.include_router(auth_router.router)


@app.get("/")
def read_root():
    """
    Endpoint raíz, simple, solo para confirmar que la API está viva.
    Útil como primer punto de prueba al levantar el servidor.
    """
    return {"message": "TaskFlow API está funcionando 🚀"}