from datetime import datetime
from typing import Any, List, Optional
from pydantic import BaseModel

class SalesTransactionBase(BaseModel):
  car_id: int
  customer_id: int
  agent_id: int
  comments: str
  
class SalesTransactionCreate(SalesTransactionBase):
  pass

class SalesTransactionUpdate(SalesTransactionBase):
  car_id: Optional[int]
  customer_id: Optional[int]
  agent_id: Optional[int]
  comments: Optional[str]

class SalesTransactionInDB(SalesTransactionBase):
  id: int
  created_at: datetime
  updated_at: datetime
  created_by: str
  updated_by: str

  model_config = {
    "from_attributes": True
  }
