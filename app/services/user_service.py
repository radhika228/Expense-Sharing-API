from sqlalchemy.orm import Session
from app.models.user import User


class UserService:
    @staticmethod
    def create_user(db: Session, name: str) -> User:
        user = User(name=name.strip())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_users(db: Session):
        return db.query(User).order_by(User.id).all()
