#use client fixture from conftest.py
def test_users_getall(client):
    response = client.get("/users/get/all")
    assert response.status_code, 403