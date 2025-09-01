from pydantic import BaseModel


class ResumesAddSchema(BaseModel):
    title: str
    content: str


class ResumesGetSchema(ResumesAddSchema):
    id: int