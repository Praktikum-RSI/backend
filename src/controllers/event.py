import uuid

from fastapi import Depends, Response

from src.dto.event import CreateEventRequest, UpdateEventRequest
from src.services.event import EventService


class EventController:
    def __init__(self, event_service: EventService = Depends(EventService)):
        self.event_service = event_service

    def create_event(self, event: CreateEventRequest) -> Response:
        result = self.event_service.create_event(event)
        response = Response(
            status_code=result.code,
            content=result.model_dump_json(),
            headers={"Content-Type": "application/json"},
        )
        return response

    def get_events(self) -> Response:
        result = self.event_service.get_events()
        response = Response(
            status_code=result.code,
            content=result.model_dump_json(),
            headers={"Content-Type": "application/json"},
        )
        return response

    def get_event_by_id(self, event_id: uuid.UUID) -> Response:
        result = self.event_service.get_event_by_id(event_id)
        response = Response(
            status_code=result.code,
            content=result.model_dump_json(),
            headers={"Content-Type": "application/json"},
        )
        return response

    def update_event(self, event_id: uuid.UUID, event: UpdateEventRequest) -> Response:
        result = self.event_service.update_event(event_id, event)
        response = Response(
            status_code=result.code,
            content=result.model_dump_json(),
            headers={"Content-Type": "application/json"},
        )
        return response

    def delete_event(self, event_id: uuid.UUID) -> Response:
        result = self.event_service.delete_event(event_id)
        response = Response(
            status_code=result.code,
            content=result.model_dump_json(),
            headers={"Content-Type": "application/json"},
        )
        return response
