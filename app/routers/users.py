from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate
from app.services.user_service import UserService

router = APIRouter(tags=["Users"])


@router.post("/users", status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = UserService.create_user(db, payload.name)
    return {"id": user.id, "name": user.name}


@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = UserService.get_users(db)
    return [{"id": user.id, "name": user.name} for user in users]
