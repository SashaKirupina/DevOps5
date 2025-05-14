from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

# Тестовые данные
test_users = [
    {"id": 1, "name": "Test User 1", "email": "test1@example.com"},
    {"id": 2, "name": "Test User 2", "email": "test2@example.com"}
]

def test_get_existed_user():
    """Тест получения существующего пользователя"""
    response = client.get("/api/v1/user", params={"email": test_users[0]["email"]})
    assert response.status_code == 200
    assert response.json() == test_users[0]

def test_get_unexisted_user():
    """Тест получения несуществующего пользователя"""
    response = client.get("/api/v1/user", params={"email": "nonexistent@example.com"})
    assert response.status_code == 404

def test_create_user_with_valid_email():
    """Тест создания пользователя с уникальным email"""
    new_user = {
        "name": "New User", 
        "email": "new.user@example.com"
    }
    response = client.post("/api/v1/user", json=new_user)
    assert response.status_code == 201
    # API возвращает просто ID (int)
    assert isinstance(response.json(), int)

def test_create_user_with_invalid_email():
    """Тест создания пользователя с существующим email"""
    duplicate_user = {
        "name": "Duplicate User",
        "email": test_users[0]["email"]  # Используем существующий email
    }
    response = client.post("/api/v1/user", json=duplicate_user)
    assert response.status_code == 409  # Conflict

def test_delete_user():
    """Тест удаления пользователя"""
    # 1. Создаем пользователя для теста
    new_user = {
        "name": "User to delete",
        "email": "delete.me@example.com"
    }
    user_id = client.post("/api/v1/user", json=new_user).json()
    
    # 2. Удаляем пользователя
    delete_response = client.delete(f"/api/v1/user/{user_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "User deleted"}
    
    # 3. Проверяем что пользователь действительно удален
    check_response = client.get(f"/api/v1/user/{user_id}")
    assert check_response.status_code == 404