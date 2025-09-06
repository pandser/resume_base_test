import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pathlib import Path


load_dotenv()
BASE_DIR = Path(__file__).parent


class AuthJWT(BaseSettings):
    '''Настройки для JWT-токена.'''
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    algorithm: str = os.getenv('ALGORITHM')
    access_token_expires_minutes: int = 15


class Settings(BaseSettings):
    '''Общие настройки приложения.'''
    # db_url: str = 'sqlite+aiosqlite:///db.sqlite3'
    db_url: str = "postgresql+asyncpg://postgres:postgres@db/postgres"
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
