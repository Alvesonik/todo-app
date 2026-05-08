
from sqlalchemy.orm import Session, sessionmaker 
from sqlalchemy import create_engine
from app.core.config import Settings

settings = Settings()
engine = create_engine(settings.DATABASE_URL)
Sessionlocal = sessionmaker[Session](bind=engine)


def get_db():
    """Функция для инъекции сессии БД"""
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()