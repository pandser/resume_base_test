from pydantic import BaseModel
from typing import Optional


class ResumesAddSchema(BaseModel):
    title: str
    content: str


class ResumesGetSchema(ResumesAddSchema):
    id: int


class ResumesOptionalSchema(BaseModel):
    title: str | None = None
    content: str | None = None
