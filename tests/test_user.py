import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# Тестовые данные
users = [{"id": 1, "name": "Test User", "email": "test@example.com"}]

def test_get_existed_user():
    response = client.get("/api/v1/user", params={"email": users[0]["email"]})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    response = client.get("/api/v1/user", params={"email": "nonexistent@mail.com"})
    assert response.status_code == 404

def test_create_user_with_valid_email():
    new_user = {"name": "New User", "email": "new.user@mail.com"}
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    assert isinstance(response.json(), int)  # Проверяем что возвращается ID (число)

def test_create_user_with_invalid_email():
    existing_email_user = {"name": "Duplicate", "email": users[0]["email"]}
    response = client.post("/api/v1/user", json=existing_email_user)
    assert response.status_code == 409  # Conflict для дубликата

def test_delete_user():
    # Создаем пользователя для удаления
    new_user = {"name": "To Delete", "email": "delete.me@mail.com"}
    user_id = client.post("/api/v1/user", json=new_user).json()
    
    # Удаляем
    delete_response = client.delete(f"/api/v1/user/{user_id}")
    assert delete_response.status_code == 200
    
    # Проверяем удаление
    check_response = client.get(f"/api/v1/user/{user_id}")
    assert check_response.status_code == 404