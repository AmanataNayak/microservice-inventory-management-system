from enum import Enum
from pydantic import BaseModel

class RoleEnum(Enum):
    READER = "reader"
    CREATOR = "creator"

class UserCreate(BaseModel):
    username: str
    password: str
    role: RoleEnum = RoleEnum.READER

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    role: RoleEnum
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
