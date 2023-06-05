
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
from db.repository.users import create_user, get_user_by_email, update_user, make_user_admin
from schemas.users import User_Create, User_Update

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
@pytest.fixture(scope="module")
def app() -> Generator[FastAPI, Any, None]:
    #setup phase
    _app = start_app()
    Base.metadata.create_all(bind=engine_test)
    yield _app
    #teardown phase
    Base.metadata.drop_all(bind=engine_test)

#this fixture starts a session in setup phase and close it in teardown phase 
#consider that this fixture is used in client fixture as input
@pytest.fixture(scope="module")
def db_session() -> Generator[Session_Test, Any, None]:
    with engine_test.connect() as connection:
        #setup phase
        #this command is necessary only for SQLite to consider integrity checks, while postgres do it by itself
        connection._dbapi_connection.cursor().execute("PRAGMA foreign_keys=ON")
        session = Session_Test(bind=connection)
        yield session
        #teardown phase
        session.close()
        connection.close()


#this fixture is used in test functions as testclient which contains db connections
#name of parameters are important to be the same as declared fixtures above (app, db_session) s-> describe above)
@pytest.fixture(scope="module")
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


#with this fixture we don't need to authenticate for every test and can simply add this to out test case as parameter
#after that use it as header in get, post, ... methods
@pytest.fixture(scope="module")
def general_auth_token_header(client : TestClient, db_session : Session_Test):
    username = "test"
    password = "123"
    email = "test@example.com"
    #create new user
    user_create = User_Create(username = username,
                              password = password,
                              email = email)
    user = get_user_by_email(email, db_session)
    if not user:
        user = create_user(user_create, db_session)

    #activate user
    update_user(user_id=user.id, user=User_Update(is_active=True), db=db_session)

    #login with new user
    input = {"username" : email,
             "password" : password,
             }
    #To send a form via post method we should use data parameter instead of json
    response = client.post("/login/token", data = input)
    auth_token = response.json()["access_token"]

    #authorization header which contains jwt joken
    auth_header = {"Authorization" : f"Bearer {auth_token}"}

    return auth_header


#with this fixture we don't need to authenticate for every test and can simply add this to out test case as parameter
#after that use it as header in get, post, ... methods
@pytest.fixture(scope="module")
def admin_auth_token_header(client : TestClient, db_session : Session_Test):
    username = "admin"
    password = "admin_pass"
    email = "admin@example.com"
    #create new user
    user_create = User_Create(username = username,
                              password = password,
                              email = email)
    user = get_user_by_email(email, db_session)
    if not user:
        user = create_user(user_create, db_session)

    #activate user
    update_user(user_id=user.id, user=User_Update(is_active=True), db=db_session)
    #admin user
    make_user_admin(user_id=user.id, db=db_session)

    #login with new user
    input = {"username" : email,
             "password" : password,
             }
    #To send a form via post method we should use data parameter instead of json
    response = client.post("/login/token", data = input)
    auth_token = response.json()["access_token"]

    #authorization header which contains jwt joken
    auth_header = {"Authorization" : f"Bearer {auth_token}"}

    return auth_header