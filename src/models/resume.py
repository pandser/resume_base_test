from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    id:  Mapped[int] = mapped_column(primary_key=True)


class ResumeModel(Base):
    __tablename__ = 'resumes'

    title: Mapped[str] = mapped_column(String(30))
    content: Mapped[str]
