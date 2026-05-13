import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Request, Response, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.controllers.event import EventController
from src.controllers.registration import RegistrationController
from src.dto.event import (
    CreateEventRequest,
    UpdateEventRequest,
)

event_router = APIRouter(prefix="/events", tags=["Events"])


@event_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_event(
    req_body: CreateEventRequest,
    controller: EventController = Depends(EventController),
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
) -> Response:
    return controller.create_event(req_body)


@event_router.get("/", status_code=status.HTTP_200_OK)
def get_events(
    controller: EventController = Depends(EventController),
) -> Response:
    return controller.get_events()


@event_router.post(
    "/{event_id}/register",
    status_code=status.HTTP_201_CREATED,
)
def register_event(
    event_id: Annotated[uuid.UUID, Path(title="The ID of the event to register")],
    request: Request,
    controller: RegistrationController = Depends(RegistrationController),
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
) -> Response:
    return controller.register_to_event(
        event_id=event_id, 
        account_id=request.state.account_id
    )


@event_router.get("/{event_id}", status_code=status.HTTP_200_OK)
def get_event(
    event_id: Annotated[uuid.UUID, Path(title="The ID of the item to get")],
    controller: EventController = Depends(EventController),
) -> Response:
    return controller.get_event_by_id(event_id)


@event_router.patch(
    "/{event_id}",
    status_code=status.HTTP_200_OK,
)
def update_event(
    event_id: Annotated[uuid.UUID, Path(title="The ID of the item to update")],
    req_body: UpdateEventRequest,
    controller: EventController = Depends(EventController),
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
) -> Response:
    return controller.update_event(event_id, req_body)


@event_router.delete(
    "/{event_id}",
    status_code=status.HTTP_200_OK,
)
def delete_event(
    event_id: Annotated[uuid.UUID, Path(title="The ID of the item to delete")],
    controller: EventController = Depends(EventController),
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
) -> Response:
    return controller.delete_event(event_id)
