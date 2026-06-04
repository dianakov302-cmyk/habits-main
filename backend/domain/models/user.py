from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    name: str
class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    verified: bool = False
    created_at: str  # Зберігаємо як ISO-рядок для простоти

    class Config:
        from_attributes = True