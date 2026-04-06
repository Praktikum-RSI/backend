import uuid

from fastapi import Depends

from src.database.models.event import Event
from src.dto.event import (
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

    def create_event(self, event: Event) -> CreateEventResponse:
        event = self.event_repository.create(event)
        return CreateEventResponse(
            code=201,
            message="Event berhasil ditambahkan",
            data=event,
        )

    def get_events(self) -> GetEventsResponse:
        events = self.event_repository.get()
        return GetEventsResponse(
            code=200,
            message="Data event berhasil diambil.",
            data=events,
        )

    def get_event_by_id(self, event_id: uuid.UUID) -> GetEventByIdResponse:
        event = self.event_repository.getById(event_id)
        return GetEventByIdResponse(
            code=200, message="Data event berhasil diambil.", data=event
        )

    def update_event(
        self, event_id: uuid.UUID, event: UpdateEventRequest
    ) -> UpdateEventResponse:
        self.event_repository.update(event_id, event)
        return UpdateEventResponse(
            code=200, message="Data event berhasil diupdate.", data=None
        )

    def delete_event(self, event_id: uuid.UUID) -> DeleteEventResponse:
        self.event_repository.delete(event_id)
        return DeleteEventResponse(
            code=200, message="Data event berhasil dihapus.", data=None
        )
