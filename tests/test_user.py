from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

test_users = [
    {"id": 1, "name": "Ivan Ivanov", "email": "i.i.ivanov@mail.com"},
    {"id": 2, "name": "Petr Petrov", "email": "p.p.petrov@mail.com"}
]

def test_get_existed_user():
    response = client.get("/api/v1/user", params={"email": test_users[0]["email"]})
    assert response.status_code == 200
    assert response.json()["email"] == test_users[0]["email"]

def test_get_unexisted_user():
    response = client.get("/api/v1/user", params={"email": "nonexistent@mail.com"})
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_create_user_with_valid_email():
    new_user = {"name": "New User", "email": "new@mail.com"}
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    assert "id" in response.json()

def test_create_user_with_invalid_email():
    existing_user = {"name": "Duplicate", "email": test_users[0]["email"]}
    response = client.post("/api/v1/user", json=existing_user)
    assert response.status_code == 409
    assert "already registered" in response.json()["detail"]

def test_delete_user():
    # Сначала создаем пользователя
    new_user = {"name": "To Delete", "email": "delete@mail.com"}
    user_id = client.post("/api/v1/user", json=new_user).json()["id"]
    
    # Удаляем
    response = client.delete(f"/api/v1/user/{user_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}
    
    # Проверяем что удален
    check_response = client.get(f"/api/v1/user", params={"email": "delete@mail.com"})
    assert check_response.status_code == 404