from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from models import Base


class ResumesModel(Base):
    __tablename__ = 'resumes'

    title: Mapped[str] = mapped_column(String(30))
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            column='users.id',
            ondelete='CASCADE',
        ),
    )
