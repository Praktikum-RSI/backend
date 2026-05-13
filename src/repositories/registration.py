import uuid

from fastapi import Depends
from sqlmodel import Session, select, func

from src.database.connection import get_session
from src.database.models.schema import Registration


class RegistrationRepository:
    def __init__(self, session: Session = Depends(get_session)) -> None:
        self.session = session

    def create(self, registration: Registration) -> Registration:
        self.session.add(registration)
        self.session.commit()
        self.session.refresh(registration)
        return registration

    def get_by_event_and_account(
        self, event_id: uuid.UUID, account_id: uuid.UUID
    ) -> Registration | None:
        return self.session.exec(
            select(Registration).where(
                Registration.event_id == event_id,
                Registration.account_id == account_id,
            )
        ).first()

    def get_by_account(self, account_id: uuid.UUID) -> list[Registration]:
        return self.session.exec(
            select(Registration).where(Registration.account_id == account_id)
        ).all()

    def count_by_event(self, event_id: uuid.UUID) -> int:
        statement = select(func.count()).select_from(Registration).where(Registration.event_id == event_id)
        return self.session.exec(statement).one()
