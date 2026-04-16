from fastapi import APIRouter, Depends, Request, Response, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.controllers.auth import AuthController
from src.dto.auth import LoginRequest, LogoutRequest, RegisterRequest

auth_router = APIRouter(tags=["Authentikasi"])


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    req_body: RegisterRequest,
    controller: AuthController = Depends(AuthController),
) -> Response:
    response = controller.register(req_body)
    return response


@auth_router.post("/login", status_code=status.HTTP_200_OK)
def login(
    req_body: LoginRequest,
    controller: AuthController = Depends(AuthController),
) -> Response:
    response = controller.login(req_body)
    return response


@auth_router.post("/logout", status_code=status.HTTP_200_OK)
def logout(
    request: Request,
    controller: AuthController = Depends(AuthController),
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
) -> Response:
    data = LogoutRequest(account_id=request.state.account_id)
    response = controller.logout(data)
    return response
