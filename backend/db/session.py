from sqlalchemy import engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from core.config import settings
from typing import Generator

engine : engine = create_engine(url=settings.DB_URL)

def get_db() -> Generator:
    try:
        db = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        yield db
    finally:
        db.close_all()