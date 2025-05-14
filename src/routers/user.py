from fastapi import APIRouter, HTTPException

router = APIRouter()

# Тестовая база данных
users_db = [
    {"id": 1, "name": "Ivan", "email": "ivan@mail.com"},
    {"id": 2, "name": "Petr", "email": "petr@mail.com"}
]

@router.get("/user")
def get_user(email: str):
    for user in users_db:
        if user["email"] == email:
            return user
    raise HTTPException(status_code=404)

@router.post("/user")
def create_user(name: str, email: str):
    if any(user["email"] == email for user in users_db):
        raise HTTPException(status_code=409)
    new_id = max(user["id"] for user in users_db) + 1
    users_db.append({"id": new_id, "name": name, "email": email})
    return {"id": new_id}

@router.delete("/user/{user_id}")
def delete_user(user_id: int):
    for i, user in enumerate(users_db):
        if user["id"] == user_id:
            users_db.pop(i)
            return {"message": "User deleted"}
    raise HTTPException(status_code=404)