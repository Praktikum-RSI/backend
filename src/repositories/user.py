from fastapi import Depends
from sqlmodel import Session

from src.database.connection import get_session
from src.database.models.user import User


class UserRepository:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    def create(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user
    