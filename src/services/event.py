import uuid

from fastapi import Depends
from starlette import status

from src.database.models.schema import Event
from src.dto.event import (
    CreateEventRequest,
    CreateEventResponse,
    DeleteEventResponse,
    GetEventByIdResponse,
    GetEventsResponse,
    UpdateEventRequest,
    UpdateEventResponse,
)
from src.repositories.event import EventRepository


class EventService:
    def __init__(self, event_repository: EventRepository = Depends(EventRepository)):
        self.event_repository = event_repository

    def create_event(self, data: CreateEventRequest) -> CreateEventResponse:
        self.event_repository.create(
            Event(
                name=data.name,
                description=data.description,
                quota=data.quota,
                started_at=data.start_date,
                end_at=data.end_date,
            )
        )
        return CreateEventResponse(
            code=status.HTTP_201_CREATED,
            data=None,
            message="Event berhasil ditambahkan",
        )

    def get_events(self) -> GetEventsResponse:
        events = self.event_repository.get()
        return GetEventsResponse(
            code=status.HTTP_200_OK,
            message="Data event berhasil diambil.",
            data=events,
        )

    def get_event_by_id(self, event_id: uuid.UUID) -> GetEventByIdResponse:
        event = self.event_repository.getById(event_id)
        return GetEventByIdResponse(
            code=status.HTTP_200_OK,
            data=event,
            message="Data event berhasil diambil.",
        )

    def update_event(
        self, event_id: uuid.UUID, event: UpdateEventRequest
    ) -> UpdateEventResponse:
        self.event_repository.update(event_id, event)
        return UpdateEventResponse(
            code=status.HTTP_200_OK, message="Data event berhasil diupdate.", data=None
        )

    def delete_event(self, event_id: uuid.UUID) -> DeleteEventResponse:
        self.event_repository.delete(event_id)
        return DeleteEventResponse(
            code=status.HTTP_200_OK, message="Data event berhasil dihapus.", data=None
        )
