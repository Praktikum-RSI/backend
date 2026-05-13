import uuid
from dataclasses import dataclass, field
from typing import Optional

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette import status
from starlette.middleware.base import BaseHTTPMiddleware

from src.utils.auth.jwt import JwtUtils


@dataclass
class ProtectedRoute:
    path: str
    methods: list[str] = field(
        default_factory=lambda: ["GET", "POST", "PUT", "PATCH", "DELETE"]
    )
    exact: bool = False

    def matches(self, path: str, method: str) -> bool:
        if method.upper() not in self.methods:
            return False
        if self.exact:
            return path == self.path
        return path.startswith(self.path)


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
        protected_routes: Optional[list[ProtectedRoute]] = None,
        admin_routes: Optional[list[ProtectedRoute]] = None,
    ) -> None:
        super().__init__(app)
        self.jwt_utils = JwtUtils()
        self.protected_routes = protected_routes or []
        self.admin_routes = admin_routes or []

    def _is_protected(self, path: str, method: str) -> bool:
        return any(route.matches(path, method) for route in self.protected_routes)

    def _is_admin_route(self, path: str, method: str) -> bool:
        return any(route.matches(path, method) for route in self.admin_routes)

    def _authenticate(self, request: Request) -> None:
        access_header = request.headers.get("Authorization")
        if not access_header or not access_header.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "data": None,
                    "message": "Token akses tidak valid",
                },
            )

        access_token = access_header.split(" ")[1]
        payload = self.jwt_utils.verify(access_token)
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "data": None,
                    "message": "Token akses tidak valid",
                },
            )

        request.state.account_id = uuid.UUID(payload["account_id"])
        request.state.role_name = payload["role_name"]

    async def dispatch(self, request: Request, call_next):
        try:
            if self._is_protected(request.url.path, request.method):
                self._authenticate(request)

            if self._is_admin_route(request.url.path, request.method):
                self._authenticate(request)

                if request.state.role_name != "ADMIN":
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail={
                            "code": status.HTTP_403_FORBIDDEN,
                            "data": None,
                            "message": "Akses ditolak",
                        },
                    )
        except HTTPException as exc:
            return JSONResponse(
                status_code=exc.status_code,
                content=exc.detail,
            )

        return await call_next(request)
