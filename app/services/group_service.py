from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.group import Group, group_members


class GroupService:
    @staticmethod
    def create_group(db: Session, name: str) -> Group:
        group = Group(name=name.strip())
        db.add(group)
        db.commit()
        db.refresh(group)
        return group

    @staticmethod
    def add_member(db: Session, group_id: int, user_id: int):
        group = db.query(Group).filter(Group.id == group_id).first()
        if group is None:
            raise HTTPException(status_code=404, detail="Group not found")

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        existing = db.execute(
            group_members.select().where(
                group_members.c.group_id == group_id,
                group_members.c.user_id == user_id,
            )
        ).first()
        if existing:
            raise HTTPException(status_code=409, detail="User is already a member")

        db.execute(group_members.insert().values(group_id=group_id, user_id=user_id))
        db.commit()
        return {"message": "Member added successfully"}

    @staticmethod
    def get_members(db: Session, group_id: int):
        group = db.query(Group).filter(Group.id == group_id).first()
        if group is None:
            raise HTTPException(status_code=404, detail="Group not found")

        return (
            db.query(User)
            .join(group_members, User.id == group_members.c.user_id)
            .filter(group_members.c.group_id == group_id)
            .order_by(User.id)
            .all()
        )
