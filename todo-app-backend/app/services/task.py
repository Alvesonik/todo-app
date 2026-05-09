from sqlalchemy.orm import Session
from app.repositories.crud import TaskRepository, CategoryRepository
from app.schemas.schemas import TaskSchema, TaskCreateSchema, TaskUpdateSchema, CategorySchema, CategoryCreateSchema, CategoryUpdateSchema   


class TaskNotFound(Exception):
    """Задача не найдена в БД"""


class TaskService:
    def __init__(self, db: Session):
        self.db = db
        self.task_repository = TaskRepository(db)

    def list_tasks(self) -> list[TaskSchema]:
        task_orms = self.task_repository.get_all()
        return [TaskSchema.model_validate(task) for task in task_orms]

    def create_task(self, task_create: TaskCreateSchema) -> TaskSchema:
        task_orm = self.task_repository.create(title=task_create.title)
        self.db.commit()
        return TaskSchema.model_validate(task_orm)

    def update_task(self, task_id: str, task_update: TaskUpdateSchema) -> TaskSchema:
        task_for_update = self.task_repository.get_by_id(task_id=task_id)
        if not task_for_update:
            raise TaskNotFound(f"Задача с id {task_id} не найдена")
        # Получаем только те поля, которые реально пришли в запросе
        update_data = task_update.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(task_for_update, field, value)

        self.db.commit() 
        self.db.refresh(task_for_update)
        return TaskSchema.model_validate(task_for_update)       

    def delete_task(self, task_id: str) ->TaskSchema:
        task_for_delete = self.task_repository.get_by_id(task_id=task_id)
        if not task_for_delete:
            raise TaskNotFound(f"Задача с id {task_id} не найдена")
        
        self.task_repository.delete(task_for_delete)
        self.db.commit()
