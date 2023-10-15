from pydantic import BaseModel, EmailStr, AnyUrl


class UserCreateRequest(BaseModel):
    name: str
    email: EmailStr


class UserCreateResponse(BaseModel):
    id: int
    token: str


class RecordCreateResponse(BaseModel):
    url: AnyUrl
