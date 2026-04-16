from fastapi import Depends
from fastapi.exceptions import HTTPException
from starlette import status

from src.database.models.schema import Account, Role, User
from src.dto.auth import (
    LoginData,
    LoginRequest,
    LoginResponse,
    LogoutRequest,
    LogoutResponse,
    RegisterRequest,
    RegisterResponse,
)
from src.repositories.account import AccountRepository
from src.repositories.role import RoleRepository
from src.repositories.user import UserRepository
from src.utils.auth.hash import HashUtils
from src.utils.auth.jwt import JwtAccessTokenPayload, JwtRefreshTokenPayload, JwtUtils


class AuthService:
    def __init__(
        self,
        userRepository: UserRepository = Depends(UserRepository),
        accountRepository: AccountRepository = Depends(AccountRepository),
        roleRepository: RoleRepository = Depends(RoleRepository),
        hashUtils: HashUtils = Depends(HashUtils),
        jwtUtils: JwtUtils = Depends(JwtUtils),
    ):
        self.userRepository = userRepository
        self.accountRepository = accountRepository
        self.roleRepository = roleRepository
        self.hashUtils = hashUtils
        self.jwtUtils = jwtUtils

    def register(self, data: RegisterRequest) -> RegisterResponse:
        role = self.roleRepository.get_by_name("USER")

        if not role:
            role = self.roleRepository.create(Role(name="USER"))

        user = self.userRepository.create(
            User(
                first_name=data.first_name,
                last_name=data.last_name,
                whatsapp_number=data.whatsapp_number,
            )
        )

        self.accountRepository.create(
            Account(
                user_id=user.id,
                role_id=role.id,
                username=data.username,
                email=data.email,
                password=self.hashUtils.hash(data.password),
            )
        )

        return RegisterResponse(
            code=status.HTTP_201_CREATED,
            message="User berhasil didaftarkan",
            data=None,
        )

    def login(self, data: LoginRequest) -> LoginResponse:
        account = self.accountRepository.get_by_email_or_username(data.identifier)

        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": status.HTTP_404_NOT_FOUND,
                    "data": None,
                    "message": "Akun tidak ditemukan",
                },
            )

        verify = self.hashUtils.verify(data.password, account.password)

        if not verify:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "code": status.HTTP_401_UNAUTHORIZED,
                    "data": None,
                    "message": "Password atau email salah",
                },
            )

        access_token = self.jwtUtils.sign(
            data=JwtAccessTokenPayload(
                account_id=str(account.id),
                role_name=account.role.name,
                ability="access_token",
            ),
        )

        refresh_token = self.jwtUtils.sign(
            data=JwtRefreshTokenPayload(
                account_id=str(account.id), ability="refresh_token"
            )
        )

        return LoginResponse(
            code=status.HTTP_200_OK,
            data=LoginData(
                access_token=access_token,
                refresh_token=refresh_token,
            ),
            message="Login berhasil",
        )

    def logout(self, data: LogoutRequest) -> LogoutResponse:
        account = self.accountRepository.get_by_id(data.account_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "code": status.HTTP_404_NOT_FOUND,
                    "data": None,
                    "message": "Akun tidak ditemukan",
                },
            )

        return LogoutResponse(
            code=status.HTTP_200_OK,
            message="Logout berhasil",
            data=None,
        )
