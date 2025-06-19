from datetime import datetime
from typing import  Any, Optional
from pydantic import BaseModel

class SystemLogsBase(BaseModel):
  user_id: int
  action: str
  timestamp: datetime
class SystemLogCreate(SystemLogsBase):
  pass

class SystemLogUpdate(SystemLogsBase):
  pass

class SystemLogsInDB(SystemLogsBase):
  id: int
  updated_at: datetime