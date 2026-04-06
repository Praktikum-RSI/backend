from datetime import datetime
from typing import Sequence

from pydantic import BaseModel, Field

from src.database.models.event import Event
from src.dto.base import BaseResponse


class CreateEventRequest(BaseModel):
    name: str = Field(default="Event Name", examples=["Event Name"])
    description: str = Field(
        default="Event Description", examples=["Event Description"]
    )
    quota: int = Field(default=100, examples=[100])
    start_date: datetime = Field(
        default_factory=datetime.now, examples=["2026-04-02T00:00:00"]
    )
    end_date: datetime = Field(
        default_factory=datetime.now, examples=["2026-04-02T00:00:00"]
    )


class CreateEventResponse(BaseResponse):
    pass


class GetEventsResponse(BaseResponse):
    data: Sequence[Event]


class GetEventByIdResponse(BaseResponse):
    data: Event


class UpdateEventRequest(BaseModel):
    name: str | None = Field(default="Event Name", examples=["Event Name"])
    description: str | None = Field(
        default="Event Description", examples=["Event Description"]
    )
    quota: int | None = Field(default=100, examples=[100])
    start_date: datetime | None = Field(
        default_factory=datetime.now, examples=["2026-04-02T00:00:00"]
    )
    end_date: datetime | None = Field(
        default_factory=datetime.now, examples=["2026-04-02T00:00:00"]
    )


class UpdateEventResponse(BaseResponse):
    pass


class DeleteEventResponse(BaseResponse):
    pass
