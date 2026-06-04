from pydantic import BaseModel, EmailStr
from typing import Optional

class GoogleAuthRequest(BaseModel):
    token: str

class UserAuth(BaseModel):
    email: EmailStr
    password: str

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class PunchCard(BaseModel):
    user_id: str
    card_type: str = "daily_habits"
    punches_earned: int = Field(default=0, ge=0, le=10)
    total_needed: int = 10
    is_completed: bool = False
    last_punch_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "card_type": "daily_habits",
                "punches_earned": 3,
                "is_completed": False
            }
        }