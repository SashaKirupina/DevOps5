from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List

router = APIRouter()

# Модели данных
class User(BaseModel):
    id: int
    name: str
    email: str

class UserCreate(BaseModel):
    name: str
    email: str

# "База данных"
db: List[User] = [
    User(id=1, name="Test User 1", email="test1@example.com"),
    User(id=2, name="Test User 2", email="test2@example.com")
]

@router.get("/user", response_model=User)
async def get_user(email: str):
    """Получение пользователя по email"""
    user = next((u for u in db if u.email == email), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("/user", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """Создание нового пользователя"""
    if any(u.email == user.email for u in db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    
    new_id = max(u.id for u in db) + 1 if db else 1
    new_user = User(id=new_id, **user.dict())
    db.append(new_user)
    return new_user.id  # Возвращаем только ID

@router.delete("/user/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(user_id: int):
    """Удаление пользователя"""
    global db
    user = next((u for u in db if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db = [u for u in db if u.id != user_id]
    return {"message": "User deleted"}