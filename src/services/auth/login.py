from fastapi import Depends
from pwdlib import PasswordHash

from src.dto.auth.login import LoginRequest, LoginResponse
from src.repositories.account import AccountRepository


class LoginService:
    def __init__(
        self,
        account_repository: AccountRepository = Depends(AccountRepository),
    ):
        self.account_repository = account_repository

    def login(self, data: LoginRequest) -> LoginResponse:
        account = self.account_repository.get_by_username(data.username)
        if not account:
            raise ValueError("Akun tidak ditemukan")

        password_hash = PasswordHash.recommended()
        verify_result = password_hash.verify(
            password=data.password, hash=account.password
        )
        if not verify_result:
            raise ValueError("Username atau password salah")

        return LoginResponse(code=200, message="Login berhasil", data=None)
