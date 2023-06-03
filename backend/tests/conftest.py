
##############################################################################
#Consider name "conftest.py" is a convention and should be use without change#
##############################################################################

import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI
from sqlalchemy import engine, create_engine
from typing import Any, Generator
from sqlalchemy.orm import sessionmaker

import sys
import os
#get the path of this file and get back 2 step in folders to add backend to paths
#this code add backend folder to places where python search for modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) 

#after backend folder has been added, we can import modules like this
from apis.base import base_router
from db.base import Base
from db.session import get_db

#create and connect to SQLite db "test_db.db" which will be placed in tests folder root
db_url = "sqlite:///./test_db.db"
engine_test = create_engine(db_url, connect_args={"check_same_thread" : False})
Session_Test = sessionmaker(bind=engine, autoflush=False, autocommit=False)

#create new app
def start_app():
    app = FastAPI(debug=True)
    app.include_router(base_router)
    return app

#fixtures can be use as input in other fixtures or test functions
#this fixture creates a new app, create all tables in setup phase and finally in teardown phase drop all tables
#consider that this fixture is using in client fixture as input
@pytest.fixture(scope="function")
def app() -> Generator[FastAPI, Any, None]:
    #setup phase
    _app = start_app()
    Base.metadata.create_all(bind=engine_test)
    yield _app
    #teardown phase
    Base.metadata.drop_all(bind=engine_test)

#this fixture starts a transaction in setup phase and rollback it in teardown phase 
#(actually in presence of drop_all, rolling back transactions would be unnecessary)
#consider that this fixture is using in client fixture as input
@pytest.fixture(scope="function")
def db_session() -> Generator[Session_Test, Any, None]:
    with engine_test.connect() as connection:
        #setup phase
        connection.begin()
        session = Session_Test(bind=connection)
        yield session
        #teardown phase
        session.close()
        connection.rollback()
        connection.close()

#this fixture is used in test functions as testclient which contains db connections
#name of parameters are important to be the same as declared fixtures above (app, db_session) s-> describe above)
@pytest.fixture(scope="function")
def client(app : FastAPI, db_session : Session_Test) -> Generator[TestClient, Any, None]:
    #here we declare a new get_db dependancy and override the original get_db with it
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    #create test client and pass it through
    with TestClient(app) as client:
        yield client

