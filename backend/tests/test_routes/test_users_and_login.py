from fastapi import status, Form
from db.repository.users import get_user_by_email
from apis.version1.route_login import create_access_token
from datetime import timedelta
from db.models.users import User

#use client fixture from conftest.py
def test_users_getall_unauthorized(client):
    response = client.get("/users/get/all")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_user_register(client):
    input = {"username" : "john",
             "password" : "123",
             "email" : "john@example.com"
             }
    response = client.post("/users/register", json = input)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == "john@example.com"
    assert response.json()["is_active"] == False

def test_user_register_badrequest(client):
    input = {"username" : "john",
             "password" : "123",
             "email" : "john.com"
             }
    response = client.post("/users/register", json = input)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "email" in response.json()["detail"][0]["msg"]

def test_change_user(client, db_session):
    #create new user
    input = {"username" : "jack",
             "password" : "123",
             "email" : "jack@example.com"
             }
    response = client.post("/users/register", json = input)
    assert response.status_code == status.HTTP_200_OK
    newuser_email : str = response.json()["email"]

    #verify and activate new user
    data = {"sub" : newuser_email}
    emailed_token = create_access_token(data, timedelta(minutes=10))
    #To send a query parameter via post or get we sholud put it in the url explicitly
    response = client.get(f"/login/verify?token={emailed_token}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg" : "Email verified seccessfully and user is now activated!"}

    #login with new user
    input = {"username" : newuser_email,
             "password" : "123"
             }
    #To send a form via post method we should use data parameter instead of json
    response = client.post("/login/token", data = input)
    assert response.status_code == status.HTTP_200_OK
    auth_token = response.json()["access_token"]

    #updating new user password
    user : User = get_user_by_email(newuser_email, db_session)
    input = {"password" : "456",
             "is_active" : True
            }
    #authorization header which contains jwt joken
    auth_header = {"Authorization" : f"Bearer {auth_token}"}
    response = client.put(f"/users/change/{user.id}", json = input, headers = auth_header)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"msg" : "Successfully updated data."}

    #get current user
    auth_header = {"Authorization" : f"Bearer {auth_token}"}
    response = client.get("/login/me", headers = auth_header)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["email"] == newuser_email

    