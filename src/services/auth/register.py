from fastapi import Depends
from pwdlib import PasswordHash

from src.database.models.account import Account
from src.database.models.role import RoleEnum
from src.database.models.user import User
from src.dto.auth.register import RegisterRequest, RegisterResponse
from src.repositories.account import AccountRepository
from src.repositories.user import UserRepository


class RegisterService:
    def __init__(
        self,
        user_repository: UserRepository = Depends(UserRepository),
        account_repository: AccountRepository = Depends(AccountRepository),
    ):
        self.user_repository = user_repository
        self.account_repository = account_repository

    def register(self, data: RegisterRequest) -> RegisterResponse:
        user_data = User(
            first_name=data.first_name,
            last_name=data.last_name,
            whatsapp_number=data.whatsapp_number,
        )

        user = self.user_repository.create(user_data)

        password_hash = PasswordHash.recommended()
        hashed_password = password_hash.hash(data.password)

        account_data = Account(
            user_id=user.id,
            role_id=RoleEnum.USER,
            email=data.email,
            username=data.username,
            password=hashed_password,
        )
        self.account_repository.create(account_data)

        return RegisterResponse(
            code=201,
            message="User registered successfully",
            data=None,
        )
