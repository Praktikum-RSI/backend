import uuid

from fastapi import Depends, HTTPException
from starlette import status

from src.database.models.schema import Registration
from src.dto.event import (
    AttendeeItem,
    GetEventAttendeesResponse,
    RegisterEventResponse,
)
from src.repositories.account import AccountRepository
from src.repositories.event import EventRepository
from src.repositories.registration import RegistrationRepository


class RegistrationService:
    def __init__(
        self,
        account_repository: AccountRepository = Depends(AccountRepository),
        event_repository: EventRepository = Depends(EventRepository),
        registration_repository: RegistrationRepository = Depends(RegistrationRepository),
    ):
        self.account_repository = account_repository
        self.event_repository = event_repository
        self.registration_repository = registration_repository

    def register_to_event(
        self, event_id: uuid.UUID, account_id: uuid.UUID
    ) -> RegisterEventResponse:
        try:
            event = self.event_repository.getById(event_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": status.HTTP_404_NOT_FOUND,
                    "data": None,
                    "message": "Event tidak ditemukan",
                },
            )

        account = self.account_repository.get_by_id(account_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": status.HTTP_404_NOT_FOUND,
                    "data": None,
                    "message": "Akun tidak ditemukan",
                },
            )

        existing_registration = self.registration_repository.get_by_event_and_account(
            event_id=event_id, account_id=account_id
        )
        if existing_registration:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": status.HTTP_400_BAD_REQUEST,
                    "data": None,
                    "message": "Anda sudah terdaftar pada event ini",
                },
            )

        total_registered = self.registration_repository.count_by_event(event_id)
        if total_registered >= event.quota:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "code": status.HTTP_400_BAD_REQUEST,
                    "data": None,
                    "message": "Kuota event sudah penuh",
                },
            )

        registration = Registration(account_id=account_id, event_id=event_id)
        self.registration_repository.create(registration)

        return RegisterEventResponse(
            code=status.HTTP_201_CREATED,
            message="Pendaftaran event berhasil",
            data=None,
        )

    def get_attendees_by_event(self, event_id: uuid.UUID) -> GetEventAttendeesResponse:
        try:
            self.event_repository.getById(event_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": status.HTTP_404_NOT_FOUND,
                    "data": None,
                    "message": "Event tidak ditemukan",
                },
            )

        rows = self.registration_repository.get_attendees_by_event(event_id)
        attendees = [
            AttendeeItem(
                registration_id=registration.id,
                account_id=account.id,
                user_id=user.id,
                email=account.email,
                username=account.username,
                first_name=user.first_name,
                last_name=user.last_name,
                whatsapp_number=user.whatsapp_number,
                registered_at=registration.created_at,
            )
            for registration, account, user in rows
        ]

        return GetEventAttendeesResponse(
            code=status.HTTP_200_OK,
            message="Data peserta event berhasil diambil.",
            data=attendees,
        )
