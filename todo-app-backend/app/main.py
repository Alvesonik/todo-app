from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models.base import Base
from app.db.session import engine
from app.api.routers.task import router as task_router
from app.core.config import Settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(task_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=Settings().allow_origins,
    allow_methods=["*"],
)


