from datetime import datetime
from typing import  Optional
from pydantic import BaseModel
from schemas.users import UserResponse


class SystemLogsResponse(BaseModel):
    id: int
    user_id: int
    action: str
    timestamp: datetime
    user: Optional[UserResponse]  # Nested user schema

    class Config:
        from_attributes = True
