import datetime
from pydantic import BaseModel, EmailStr
from pydantic.config import ConfigDict
from app.schemas.role import UserRole

class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    role: UserRole = UserRole.USER

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    role: UserRole
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"