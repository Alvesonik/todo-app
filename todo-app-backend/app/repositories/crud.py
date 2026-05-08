from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import TaskORM, CategoryORM


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[TaskORM]:
        return self.db.scalars(select(TaskORM)).all()

    def get_by_id(self, task_id: str) -> TaskORM:
        return self.db.get(TaskORM, task_id)

    def create(self, title: str) -> TaskORM:
        new_task = TaskORM(title=title, completed=False)
        self.db.add(new_task)
        return new_task

    def delete(self, TaskORM) -> None:
        self.db.delete(TaskORM)


class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[CategoryORM]:
        return self.db.scalars(select(CategoryORM)).all()

    def get_by_id(self, category_id: str) -> CategoryORM:
        return self.db.get(CategoryORM, category_id)

    def create(self, name: str) -> CategoryORM:
        new_cat = CategoryORM(name=name)
        self.db.add(new_cat)
        self.db.commit()

    def delete(self, CategoryORM) -> None:
        self.db.delete(CategoryORM)        