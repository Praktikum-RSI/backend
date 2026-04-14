from fastapi import Depends, status
from fastapi.routing import APIRouter

from src.controllers.auth.login import LoginController
from src.controllers.auth.register import RegisterController
from src.dto.auth.login import LoginRequest
from src.dto.auth.register import RegisterRequest

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/")
async def login(
    data: LoginRequest, controller: LoginController = Depends(LoginController)
):
    return controller.login(data)


@auth_router.post("/", status_code=status.HTTP_201_CREATED)
def register(
    data: RegisterRequest, controller: RegisterController = Depends(RegisterController)
):
    return controller.register(data)
