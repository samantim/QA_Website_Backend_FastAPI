from db.session import engine
from db.base import Base
from fastapi import FastAPI
from apis.base import base_router

def create_table():
    Base.metadata.create_all(engine)

def include_routers(app : FastAPI):
    app.include_router(base_router)

def start_app() -> FastAPI:
    app = FastAPI(debug=True)
    create_table()
    include_routers(app)
    return app 


app = start_app()



