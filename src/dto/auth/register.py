from pydantic import BaseModel, EmailStr

from src.dto.base import BaseResponse


class RegisterRequest(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    username: str
    password: str
    whatsapp_number: str


class RegisterResponse(BaseResponse):
    pass
