from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class UsersModel(Base):
    __tablename__ = 'users'

    username: Mapped[str] = mapped_column(String(30))
    email: Mapped[str]
    password: Mapped[str]
