import uuid
from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from src.database.models.role import Role, RoleEnum


class Account(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID | None = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="account")
    role_id: RoleEnum | None = Field(default=None, foreign_key="role.name")
    role: Role | None = Relationship(back_populates="accounts")
    email: str
    username: str
    password: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
