from passlib.context import CryptContext
from core.config import settings

#context need for all hashing capabilities
pwd_context = CryptContext(schemes=["bcrypt"])

class Hasher:

    #take a plain password and hash it
    #using static method to use class without instantiation
    @staticmethod
    def hash_password(plain_password : str) -> str:
        return pwd_context.hash(plain_password)

    #compare palin and hashed password to figure out they are the same or not
    #hint : hashed password is never decrypted
    @staticmethod
    def verify_password(plain_password : str, hashed_password : str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)