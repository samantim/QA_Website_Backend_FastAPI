from sqlalchemy import engine, create_engine
from sqlalchemy.orm import Session, sessionmaker
from core.config import settings
from typing import Generator

#here we keep database session

engine : engine = create_engine(url=settings.DB_URL)
#engine = create_engine("sqlite:///./test_db.db")

session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)

#the method which use as dependency in all db transactions
def get_db() -> Generator:
    try:
        #recreate session an keep it in memory
        db = session_local()
        yield db
    finally:
        db.close()