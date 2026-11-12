from sqlalchemy import Column, Integer, String, ForeignKey, Table, UniqueConstraint
from app.database import Base

group_members = Table(
    "group_members",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id"), nullable=False),
    Column("user_id", Integer, ForeignKey("users.id"), nullable=False),
    UniqueConstraint("group_id", "user_id", name="uq_group_user"),
)


class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
