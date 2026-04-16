from fastapi import Depends, Response

from src.dto.auth import LoginRequest, LogoutRequest, RegisterRequest
from src.services.auth import AuthService


class AuthController:
    def __init__(self, auth_service: AuthService = Depends(AuthService)):
        self.auth_service = auth_service

    def register(self, req_body: RegisterRequest) -> Response:
        register = self.auth_service.register(req_body)
        response = Response(
            status_code=register.code,
            content=register.model_dump_json(),
            headers={"Content-Type": "application/json"},
        )
        return response

    def login(self, req_body: LoginRequest) -> Response:
        login = self.auth_service.login(req_body)
        response = Response(
            status_code=login.code,
            content=login.model_dump_json(),
            headers={"Content-Type": "application/json"},
        )
        response.set_cookie(key="access_token", value=login.data.access_token)
        response.set_cookie(key="refresh_token", value=login.data.refresh_token)
        return response

    def logout(
        self,
        data: LogoutRequest,
    ) -> Response:
        logout = self.auth_service.logout(data)
        response = Response(
            status_code=logout.code,
            content=logout.model_dump_json(),
            headers={"Content-Type": "application/json"},
        )
        response.delete_cookie(key="access_token")
        response.delete_cookie(key="refresh_token")
        return response
