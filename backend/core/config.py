import os
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(".")/".env"
load_dotenv(dotenv_path=env_path)

print(env_path.absolute())

class Settings:
    DB_TYPE : str = os.getenv("db_type")
    DB_USERNAME : str = os.getenv("db_username")
    DB_PASSWORD : str = os.getenv("db_password")
    DB_HOST : str = os.getenv("db_host")
    DB_PORT : str = os.getenv("db_port")
    DB_NAME : str = os.getenv("db_name")

    DB_URL : str = f"{DB_TYPE}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

settings = Settings()