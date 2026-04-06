import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Path, status

from src.controllers.event import EventController
from src.dto.event import (
    CreateEventRequest,
    CreateEventResponse,
    DeleteEventResponse,
    GetEventByIdResponse,
    GetEventsResponse,
    UpdateEventRequest,
    UpdateEventResponse,
)

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_event(
    req_body: CreateEventRequest, controller: EventController = Depends(EventController)
) -> CreateEventResponse:
    return controller.create_event(req_body)


@router.get("/", status_code=status.HTTP_200_OK)
def get_events(
    controller: EventController = Depends(EventController),
) -> GetEventsResponse:
    return controller.get_events()


@router.get("/{event_id}")
def get_event(
    event_id: Annotated[uuid.UUID, Path(title="The ID of the item to get")],
    controller: EventController = Depends(EventController),
) -> GetEventByIdResponse:
    return controller.get_event_by_id(event_id)


@router.patch("/{event_id}")
def update_event(
    event_id: Annotated[uuid.UUID, Path(title="The ID of the item to update")],
    req_body: UpdateEventRequest,
    controller: EventController = Depends(EventController),
) -> UpdateEventResponse:
    return controller.update_event(event_id, req_body)


@router.delete("/{event_id}")
def delete_event(
    event_id: Annotated[uuid.UUID, Path(title="The ID of the item to delete")],
    controller: EventController = Depends(EventController),
) -> DeleteEventResponse:
    return controller.delete_event(event_id)
