from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class ResumeModel(Base):
    __tablename__ = 'resumes'

    title: Mapped[str] = mapped_column(String(30))
    content: Mapped[str]
