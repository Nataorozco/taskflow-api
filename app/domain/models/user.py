from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


class User(BaseModel):
    id: int | None = None
    email: EmailStr
    full_name: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)