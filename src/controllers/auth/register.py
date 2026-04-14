from fastapi import Depends

from src.dto.auth.register import RegisterRequest
from src.services.auth.register import RegisterService


class RegisterController:
    def __init__(self, register_service: RegisterService = Depends(RegisterService)):
        self.register_service = register_service

    def register(self, data: RegisterRequest):
        response = self.register_service.register(data)
        return response
