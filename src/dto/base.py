from typing import Any

from pydantic import BaseModel


class BaseResponse(BaseModel):
    code: int
    message: str
    data: Any
