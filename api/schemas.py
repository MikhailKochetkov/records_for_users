from pydantic import BaseModel, EmailStr, FilePath


class UserCreateRequest(BaseModel):
    name: str
    email: EmailStr


class UserCreateResponse(BaseModel):
    id: int
    token: str


class RecordCreateRequest(BaseModel):
    user_id: int
    token: str
    audio: FilePath


class RecordCreateResponse(BaseModel):
    url: str
