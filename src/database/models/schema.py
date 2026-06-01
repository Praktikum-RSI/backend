import uuid
from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel


class AuditLog(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    request_id: str | None
    method: str
    path: str
    query_params: str | None
    status_code: int
    duration_ms: float
    client_ip: str | None
    user_agent: str | None
    account_id: uuid.UUID | None
    content_type: str | None
    created_at: datetime = Field(default_factory=datetime.now)


class Role(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(unique=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    accounts: list["Account"] = Relationship(back_populates="role")


class User(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    first_name: str
    last_name: str
    whatsapp_number: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    accounts: list["Account"] = Relationship(back_populates="user")


class Account(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    role_id: uuid.UUID = Field(foreign_key="role.id")
    email: str = Field(unique=True)
    username: str = Field(unique=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    user: User = Relationship(back_populates="accounts")
    role: Role = Relationship(back_populates="accounts")
    registrations: list["Registration"] = Relationship(back_populates="account")


class Event(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    description: str
    quota: int
    started_at: datetime
    end_at: datetime
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    registrations: list["Registration"] = Relationship(back_populates="event")


class Registration(SQLModel, table=True):
    __table_args__ = {"extend_existing": True}
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    account_id: uuid.UUID = Field(foreign_key="account.id")
    event_id: uuid.UUID = Field(foreign_key="event.id")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    account: "Account" = Relationship(back_populates="registrations")
    event: Event = Relationship(back_populates="registrations")
