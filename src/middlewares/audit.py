import logging
import time
import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from src.database.connection import get_session
from src.database.models.schema import AuditLog

logger = logging.getLogger("audit")


class AuditMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, exclude_paths: list[str] | None = None):
        super().__init__(app)
        self.exclude_paths = exclude_paths or []

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if request.url.path in self.exclude_paths:
            return await call_next(request)

        request_id = str(uuid.uuid4())
        start_time = time.perf_counter()
        request.state.request_id = request_id

        status_code: int | None = None

        try:
            response = await call_next(request)
            status_code = response.status_code
            duration_ms = (time.perf_counter() - start_time) * 1000
            await self._save_log(
                request=request,
                request_id=request_id,
                status_code=500,
                duration_ms=duration_ms,
            )
        except Exception:
            raise

        duration_ms = (time.perf_counter() - start_time) * 1000
        response.headers["X-Request-ID"] = request_id

        await self._save_log(
            request=request,
            request_id=request_id,
            status_code=status_code,
            duration_ms=duration_ms,
        )

        return response

    async def _save_log(
        self,
        request: Request,
        request_id: str,
        status_code: int | None,
        duration_ms: float,
    ) -> None:
        account_id: str | None = getattr(request.state, "account_id", None)
        logger.info("DEBUG account_id: %s", account_id)
        logger.info("DEBUG state keys: %s", request.state._state)
        log_entry = AuditLog(
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            query_params=str(request.query_params) or None,
            status_code=status_code,
            duration_ms=round(duration_ms, 2),
            client_ip=self._get_client_ip(request),
            user_agent=request.headers.get("user-agent"),
            account_id=account_id,
        )
        try:
            with next(get_session()) as session:
                session.add(log_entry)
                session.commit()
        except Exception as exc:
            logger.error("Failed to save audit log: %s", exc)

    def _get_client_ip(self, request: Request) -> str:
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        return request.client.host if request.client else "unknown"
