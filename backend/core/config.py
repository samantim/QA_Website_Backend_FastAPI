import os
from pathlib import Path
from dotenv import load_dotenv

#create a path of .env file and load it
env_path = Path(".")/".env"
load_dotenv(dotenv_path=env_path)

#keeping all private info and config here
#this file must be excluded from git (.gitignore)
class Settings:
    DB_TYPE : str = os.getenv("db_type")
    DB_USERNAME : str = os.getenv("db_username")
    DB_PASSWORD : str = os.getenv("db_password")
    DB_HOST : str = os.getenv("db_host")
    DB_PORT : str = os.getenv("db_port")
    DB_NAME : str = os.getenv("db_name")
    DB_URL : str = f"{DB_TYPE}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    EMAIL_HOST = os.getenv("email_host")
    EMAIL_PORT = os.getenv("email_port")
    EMAIL_USERNAME = os.getenv("email_username")
    EMAIL_PASSWORD = os.getenv("email_password")


    JWT_SECRET_KEY = os.getenv("jwt_secret_key")
    JWT_ALGORITHMS = os.getenv("jwt_algorithms")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTE = int(os.getenv("jwt_access_token_expire_minute"))
    

settings = Settings()