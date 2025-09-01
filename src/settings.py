from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = 'sqlite+aiosqlite:///src/db.sqlite3'


settings = Settings()
