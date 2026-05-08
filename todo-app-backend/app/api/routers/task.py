
from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.schemas import TaskSchema, TaskCreateSchema, TaskUpdateSchema, CategorySchema, CategoryCreateSchema, CategoryUpdateSchema
from app.services.task import TaskService, TaskNotFound
from app.api.dependencies import get_task_service


router = APIRouter(prefix="/tasks")


@router.get("")
def read_tasks(task_service: TaskService = Depends(get_task_service)) -> list[TaskSchema]:
    return task_service.list_tasks()

@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreateSchema, 
    task_service: TaskService = Depends(get_task_service)
) -> TaskSchema:
    return task_service.create_task(task_create=payload)

@router.patch("/{task_id}")
def update_task( 
    task_id: str, 
    payload: TaskUpdateSchema,
    task_service: TaskService = Depends(get_task_service)
) -> TaskSchema:
    try:
        return task_service.update_task(task_id=task_id, task_update=payload)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, task_service: TaskService = Depends(get_task_service)) -> None:
    try:
        return task_service.delete_task(task_id=task_id)
    except TaskNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


# @router.get("/categories")
# def read_categories() -> list[CategorySchema]:
#     ...


# @router.post("/categories", status_code=status.HTTP_201_CREATED)
# def create_category(payload: CategoryCreateSchema) -> CategorySchema:
#    ...


# @router.patch("/categories/{category_id}")
# def update_category(payload: CategoryUpdateSchema, category_id: str) -> CategorySchema:
 #   ...

# @router.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_category(category_id: str) -> None:
#    ...