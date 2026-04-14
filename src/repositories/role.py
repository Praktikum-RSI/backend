from fastapi import Depends
from sqlmodel import Session

from src.database.connection import get_session
from src.database.models.role import Role


class RoleRepository:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    def create(self, role: Role):
        self.session.add(role)
        self.session.commit()
        self.session.refresh(role)
        return role
