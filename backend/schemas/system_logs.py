from datetime import datetime
from typing import  Optional
from pydantic import BaseModel
from schemas.users import UserResponse


class SystemLogsResponse(BaseModel):
  id: int
  user_id: int
  action: str
  timestamp: datetime
  user: Optional[UserResponse]
  
  model_config = {
    "from_attributes": True
  }


class SystemLogCreate(BaseModel):
  user_id: int
  action: str
  timestamp: datetime