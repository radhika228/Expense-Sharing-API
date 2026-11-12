from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.group import GroupCreate, MemberCreate
from app.services.group_service import GroupService

router = APIRouter(tags=["Groups"])


@router.post("/groups", status_code=201)
def create_group(payload: GroupCreate, db: Session = Depends(get_db)):
    group = GroupService.create_group(db, payload.name)
    return {"id": group.id, "name": group.name}


@router.post("/groups/{group_id}/members")
def add_member(group_id: int, payload: MemberCreate, db: Session = Depends(get_db)):
    return GroupService.add_member(db, group_id, payload.user_id)


@router.get("/groups/{group_id}/members")
def get_group_members(group_id: int, db: Session = Depends(get_db)):
    members = GroupService.get_members(db, group_id)
    return [{"id": user.id, "name": user.name} for user in members]
