import uuid

from fastapi import Depends, Response

from src.dto.event import RegisterEventResponse
from src.services.registration import RegistrationService


class RegistrationController:
    def __init__(self, registration_service: RegistrationService = Depends(RegistrationService)):
        self.registration_service = registration_service

    def register_to_event(self, event_id: uuid.UUID) -> Response:
        result = self.registration_service.register_to_event(event_id)
        response = Response(
            status_code=result.code,
            content=result.model_dump_json(),
            headers={"Content-Type": "application/json"},
        )
        return response
