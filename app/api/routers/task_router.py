from fastapi import APIRouter, Depends, HTTPException
from app.api.schemas.task_schemas import TaskCreate, TaskResponse
from app.api.dependencies import get_task_repository
from app.domain.repositories.task_repository import TaskRepository
from app.domain.models.task import Task

# APIRouter agrupa endpoints relacionados (todos los de "tasks" aquí),
# para luego "montarlos" todos juntos en la app principal (main.py).
# prefix="/tasks" significa que todas las rutas de este router empiezan
# con /tasks automáticamente (ej. POST /tasks, GET /tasks/1).
router = APIRouter(prefix="/tasks", tags=["tasks"])

# TEMPORAL: hasta que exista autenticación real, todas las tareas se
# asignan a este owner_id fijo. Cuando se implemente login/JWT, esto
# se reemplaza por el id del usuario autenticado en cada petición.
TEMP_OWNER_ID = 1


@router.post("/", response_model=TaskResponse)
def create_task(
    task_data: TaskCreate,
    repo: TaskRepository = Depends(get_task_repository)
):
    """
    Crea una nueva tarea.

    task_data: TaskCreate — FastAPI valida automáticamente que el
    cuerpo de la petición (JSON) tenga esta forma exacta; si falta un
    campo obligatorio o el tipo no coincide, FastAPI responde con un
    error 422 antes de que esta función siquiera se ejecute.

    repo: TaskRepository = Depends(get_task_repository) — FastAPI
    resuelve automáticamente esta dependencia: llama a
    get_task_repository(), que a su vez llama a get_db(), y termina
    entregando aquí un SQLAlchemyTaskRepository listo para usar.
    """
    # Convertimos el schema de entrada (TaskCreate) en un Task de
    # dominio, agregando el owner_id que el cliente no envía.
    task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        due_date=task_data.due_date,
        owner_id=TEMP_OWNER_ID,
    )
    saved_task = repo.save(task)
    return saved_task


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    repo: TaskRepository = Depends(get_task_repository)
):
    """
    Busca una tarea por su id.
    Si no existe, responde con un 404 explícito en vez de devolver
    null o una lista vacía — es más claro para quien consume la API.
    """
    task = repo.get_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task


@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    repo: TaskRepository = Depends(get_task_repository)
):
    """
    Lista todas las tareas del usuario actual (TEMP_OWNER_ID por ahora).
    """
    return repo.get_all_by_owner(TEMP_OWNER_ID)


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    repo: TaskRepository = Depends(get_task_repository)
):
    """
    Elimina una tarea por su id.
    Igual que get_task, responde 404 si no existe — eliminar algo que
    nunca existió no debería reportarse como un éxito silencioso.
    """
    deleted = repo.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return {"success": True, "message": f"Tarea {task_id} eliminada"}