from fastapi import APIRouter, Depends, status, HTTPException
from app.schemas.schemas import (
    TaskSchema, TaskCreateSchema, TaskUpdateSchema,
    CategorySchema, CategoryCreateSchema, CategoryUpdateSchema
)
from app.services.task import TaskService, CategoryService, TaskNotFound, CategoryNotFound
from app.api.dependencies import get_task_service, get_category_service

tasks_router = APIRouter(prefix="/tasks")
categories_router = APIRouter(prefix="/categories")


# === Tasks ===
@tasks_router.get("", response_model=list[TaskSchema])
async def read_tasks(task_service: TaskService = Depends(get_task_service)):
    return await task_service.list_tasks()


@tasks_router.post("", status_code=status.HTTP_201_CREATED, response_model=TaskSchema)
async def create_task(
    payload: TaskCreateSchema,
    task_service: TaskService = Depends(get_task_service)
):
    return await task_service.create_task(payload)


@tasks_router.patch("/{task_id}", response_model=TaskSchema)
async def update_task(
    task_id: str,
    payload: TaskUpdateSchema,
    task_service: TaskService = Depends(get_task_service)
):
    try:
        return await task_service.update_task(task_id, payload)
    except TaskNotFound:
        raise HTTPException(status_code=404, detail="Task not found")


@tasks_router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    task_service: TaskService = Depends(get_task_service)
):
    try:
        await task_service.delete_task(task_id)
    except TaskNotFound:
        raise HTTPException(status_code=404, detail="Task not found")


# === Categories ===
@categories_router.get("", response_model=list[CategorySchema])
async def read_categories(category_service: CategoryService = Depends(get_category_service)):
    return await category_service.list_category()


@categories_router.post("", status_code=status.HTTP_201_CREATED, response_model=CategorySchema)
async def create_category(
    payload: CategoryCreateSchema,
    category_service: CategoryService = Depends(get_category_service)
):
    return await category_service.create_category(payload)


@categories_router.patch("/{category_id}", response_model=CategorySchema)
async def update_category(
    category_id: str,
    payload: CategoryUpdateSchema,
    category_service: CategoryService = Depends(get_category_service)
):
    try:
        return await category_service.update_category(category_id, payload)
    except CategoryNotFound:
        raise HTTPException(status_code=404, detail="Category not found")


@categories_router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: str,
    category_service: CategoryService = Depends(get_category_service)
):
    try:
        await category_service.delete_category(category_id)
    except CategoryNotFound:
        raise HTTPException(status_code=404, detail="Category not found")