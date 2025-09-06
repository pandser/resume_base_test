from pydantic import BaseModel, EmailStr


class UsersSchema(BaseModel):
    usesrname: str
    email: EmailStr

class UsersGetSchema(UsersSchema):
    user_id: int


class UsersInDBSchema(UsersSchema):
    password: str
