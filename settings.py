import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path


load_dotenv()
BASE_DIR = Path(__file__).parent
DB_NAME=os.getenv('DB_NAME')
POSTGRES_USER=os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD=os.getenv('POSTGRES_PASSWORD')
DB_HOST=os.getenv('DB_HOST')


class AuthJWT(BaseSettings):
    '''Настройки для JWT-токена.'''
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    algorithm: str = os.getenv('ALGORITHM')
    access_token_expires_minutes: int = 15


class Settings(BaseSettings):
    '''Общие настройки приложения.'''
    db_url: str = (f"postgresql+asyncpg://{POSTGRES_USER}:"
                    f"{POSTGRES_PASSWORD}@{DB_HOST}/{DB_NAME}")
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
