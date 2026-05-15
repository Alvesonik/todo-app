from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.crud import TaskRepository, CategoryRepository
from app.schemas.schemas import (
    TaskSchema, TaskCreateSchema, TaskUpdateSchema,
    CategorySchema, CategoryCreateSchema, CategoryUpdateSchema
)


class TaskNotFound(Exception):
    pass

class CategoryNotFound(Exception):
    pass


class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = TaskRepository(db)

    async def list_tasks(self) -> list[TaskSchema]:
        tasks = await self.repo.get_all()
        return [TaskSchema.model_validate(t) for t in tasks]

    async def create_task(self, task_create: TaskCreateSchema) -> TaskSchema:
        task_orm = await self.repo.create(title=task_create.title)
        await self.db.commit()
        await self.db.refresh(task_orm)
        return TaskSchema.model_validate(task_orm)

    async def update_task(self, task_id: str, task_update: TaskUpdateSchema) -> TaskSchema:
        task = await self.repo.get_by_id(task_id)
        if not task:
            raise TaskNotFound(f"Задача {task_id} не найдена")

        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        await self.db.commit()
        await self.db.refresh(task)
        return TaskSchema.model_validate(task)

    async def delete_task(self, task_id: str) -> None:
        task = await self.repo.get_by_id(task_id)
        if not task:
            raise TaskNotFound(f"Задача {task_id} не найдена")
        await self.repo.delete(task)
        await self.db.commit()


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = CategoryRepository(db)

    async def list_category(self) -> list[CategorySchema]:
        cats = await self.repo.get_all()
        return [CategorySchema.model_validate(c) for c in cats]

    async def create_category(self, category_create: CategoryCreateSchema) -> CategorySchema:
        cat_orm = await self.repo.create(name=category_create.name)
        await self.db.commit()
        await self.db.refresh(cat_orm)
        return CategorySchema.model_validate(cat_orm)

    async def update_category(self, category_id: str, category_update: CategoryUpdateSchema) -> CategorySchema:
        cat = await self.repo.get_by_id(category_id)
        if not cat:
            raise CategoryNotFound(f"Категория {category_id} не найдена")

        update_data = category_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(cat, field, value)

        await self.db.commit()
        await self.db.refresh(cat)
        return CategorySchema.model_validate(cat)

    async def delete_category(self, category_id: str) -> None:
        cat = await self.repo.get_by_id(category_id)
        if not cat:
            raise CategoryNotFound(f"Категория {category_id} не найдена")
        await self.repo.delete(cat)
        await self.db.commit()