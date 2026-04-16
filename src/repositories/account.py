import uuid

from fastapi import Depends
from sqlmodel import Session, select

from src.database.connection import get_session
from src.database.models.schema import Account


class AccountRepository:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    def create(self, account: Account):
        self.session.add(account)
        self.session.commit()
        self.session.refresh(account)
        return account

    def get_by_id(self, account_id: uuid.UUID) -> Account | None:
        account = self.session.exec(
            select(Account).where(Account.id == account_id)
        ).first()
        return account

    def get_by_email_or_username(self, identifier: str) -> Account | None:
        account = self.session.exec(
            select(Account).where(
                Account.email == identifier or Account.username == identifier
            )
        ).first()
        return account
