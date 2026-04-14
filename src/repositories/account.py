from fastapi import Depends
from sqlmodel import Session, select

from src.database.connection import get_session
from src.database.models.account import Account


class AccountRepository:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    def create(self, account: Account):
        self.session.add(account)
        self.session.commit()
        self.session.refresh(account)
        return account

    def get_by_username(self, username: str) -> Account | None:
        account = self.session.exec(
            select(Account).where(Account.username == username)
        ).first()
        return account
