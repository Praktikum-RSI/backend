from pydantic import BaseModel

from src.dto.base import BaseResponse


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseResponse):
    pass
