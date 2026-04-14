from fastapi.param_functions import Depends

from src.dto.auth.login import LoginRequest
from src.services.auth.login import LoginService


class LoginController:
    def __init__(self, login_service: LoginService = Depends(LoginService)):
        self.login_service = login_service

    def login(self, data: LoginRequest):
        response = self.login_service.login(data)
        return response
