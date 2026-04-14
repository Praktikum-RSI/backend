import enum

from sqlmodel import Field, Relationship, SQLModel


class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"


class Role(SQLModel, table=True):
    name: RoleEnum = Field(default=RoleEnum.USER, primary_key=True)
    accounts: list["Account"] = Relationship(back_populates="role")
