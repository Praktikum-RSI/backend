from fastapi import Depends, Request

from src.utils.auth.jwt import JWT


class AccessTokenMiddleware:
    def __init__(self, jwtUtils: JWT = Depends(JWT)) -> None:
        self.jwtUtils = jwtUtils

    def verify_access_token(self, request: Request, call_next):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return {"error": "Permintaan tidak terautorisasi"}

        auth_token = auth_header.split(" ")
        if auth_token[0] != "Bearer":
            return {"error": "Token autorisasi tidak valid"}

        access_token = auth_token[1]
        payload = self.jwtUtils.verify(access_token)
        if not payload:
            return {"error": "Token akses tidak valid"}

        if payload.get("ability") != "access_token":
            return {"error": "Token akses tidak valid"}

        request.state.user = payload
        return call_next(request)
