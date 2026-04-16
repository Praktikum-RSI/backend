from pwdlib import PasswordHash


class HashUtils:
    def __init__(self):
        self.password_hash = PasswordHash.recommended()

    def hash(self, password: str) -> str:
        return self.password_hash.hash(password)

    def verify(self, password: str, hash: str) -> bool:
        return self.password_hash.verify(password, hash)
