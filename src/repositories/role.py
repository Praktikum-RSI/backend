from fastapi import Depends
from sqlmodel import Session, select

from src.database.connection import get_session
from src.database.models.schema import Role


class RoleRepository:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    def create(self, role: Role):
        self.session.add(role)
        self.session.commit()
        self.session.refresh(role)
        return role

    def get_by_name(self, name: str) -> Role | None:
        role = self.session.exec(select(Role).where(Role.name == name)).first()
        return role
