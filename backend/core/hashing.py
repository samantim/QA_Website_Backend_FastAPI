from passlib.context import CryptContext
from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"])

class Hasher:

    @staticmethod
    def hash_password(plain_password : str) -> str:
        return pwd_context.hash(plain_password)

    @staticmethod
    def verify_password(plain_password : str, hashed_password : str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)