import uuid

from fastapi import Depends

from src.database.models.event import Event
from src.dto.event import CreateEventRequest, UpdateEventRequest
from src.services.event import EventService


class EventController:
    def __init__(self, event_service: EventService = Depends(EventService)):
        self.event_service = event_service

    def create_event(self, event: CreateEventRequest):
        event_data = Event(
            name=event.name,
            description=event.description,
            quota=event.quota,
            started_at=event.start_date,
            end_at=event.end_date,
        )
        response = self.event_service.create_event(event_data)
        return response

    def get_events(self):
        response = self.event_service.get_events()
        return response

    def get_event_by_id(self, event_id: uuid.UUID):
        response = self.event_service.get_event_by_id(event_id)
        return response

    def update_event(self, event_id: uuid.UUID, event: UpdateEventRequest):
        response = self.event_service.update_event(event_id, event)
        return response

    def delete_event(self, event_id: uuid.UUID):
        response = self.event_service.delete_event(event_id)
        return response
