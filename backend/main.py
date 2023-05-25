from db.session import engine
from db.base import Base
from fastapi import FastAPI
from sqlalchemy import MetaData

def create_table():
    Base.metadata.create_all(engine)
    

app = FastAPI()
create_table()
