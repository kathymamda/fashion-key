from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8)

class UserInDB(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    hashed_password: str
    created_at: datetime
    profile_picture: Optional[str] = None
    body_measurements: Optional[dict] = None
    fashion_preferences: Optional[list] = []
    is_active: bool = True

class UserResponse(BaseModel):
    id: Optional[str] = None
    name: str
    email: str
    created_at: datetime
    profile_picture: Optional[str] = None
