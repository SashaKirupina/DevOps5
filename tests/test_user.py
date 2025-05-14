from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

test_users = [
    {"id": 1, "name": "Ivan", "email": "ivan@mail.com"},
    {"id": 2, "name": "Petr", "email": "petr@mail.com"}
]

def test_get_existed_user():
    response = client.get("/user", params={"email": "ivan@mail.com"})
    assert response.status_code == 200
    assert response.json()["email"] == "ivan@mail.com"

def test_get_unexisted_user():
    response = client.get("/user", params={"email": "none@mail.com"})
    assert response.status_code == 404

def test_create_user_with_valid_email():
    response = client.post("/user?name=New&email=new@mail.com")
    assert response.status_code == 200
    assert "id" in response.json()

def test_create_user_with_invalid_email():
    response = client.post("/user?name=Duplicate&email=ivan@mail.com")
    assert response.status_code == 409

def test_delete_user():
    # Сначала создаем пользователя
    create_res = client.post("/user?name=ToDelete&email=delete@mail.com")
    user_id = create_res.json()["id"]
    
    # Удаляем
    delete_res = client.delete(f"/user/{user_id}")
    assert delete_res.status_code == 200
    assert delete_res.json() == {"message": "User deleted"}