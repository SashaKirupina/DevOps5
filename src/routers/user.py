from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get("/user")
async def get_user(email: str):
    test_users = [
        {"id": 1, "name": "Ivan", "email": "i.i.ivanov@mail.com"},
        {"id": 2, "name": "Petr", "email": "p.p.petrov@mail.com"}
    ]
    
    for user in test_users:
        if user["email"] == email:
            return user
    raise HTTPException(status_code=404, detail="User not found")