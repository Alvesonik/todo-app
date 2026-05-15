from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import TaskORM, CategoryORM


class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[TaskORM]:
        result = await self.db.execute(select(TaskORM))
        return result.scalars().all()

    async def get_by_id(self, task_id: str) -> TaskORM | None:
        return await self.db.get(TaskORM, task_id)

    async def create(self, title: str) -> TaskORM:
        new_task = TaskORM(title=title, completed=False)
        self.db.add(new_task)
        return new_task

    async def delete(self, task: TaskORM) -> None:
        await self.db.delete(task)


class CategoryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[CategoryORM]:
        result = await self.db.execute(select(CategoryORM))
        return result.scalars().all()

    async def get_by_id(self, category_id: str) -> CategoryORM | None:
        return await self.db.get(CategoryORM, category_id)

    async def create(self, name: str) -> CategoryORM:
        new_category = CategoryORM(name=name)
        self.db.add(new_category)
        return new_category

    async def delete(self, category: CategoryORM) -> None:
        await self.db.delete(category)