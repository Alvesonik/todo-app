from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.task import TaskService, CategoryService


async def get_task_service(db: AsyncSession = Depends(get_db)) -> TaskService:
    """Функция для инъекции зависимости TaskService"""
    return TaskService(db)

async def get_category_service(db: AsyncSession = Depends(get_db)) -> CategoryService:
    """Функция для инъекции зависимости CategoryService"""
    return CategoryService(db)