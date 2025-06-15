from pydantic import BaseModel
from typing import Optional
from schemas.users import UserResponse
from schemas.cars import CarResponse


class SalesTransactionResponse(BaseModel):
  id: int
  car_id: int
  customer_id: int
  agent_id: int
  comments: str

  car: Optional[CarResponse] = None
  customer: Optional[UserResponse] = None
  agent: Optional[UserResponse] = None

  model_config = {
    "from_attributes": True
  }

class SalesTransactionCreate(BaseModel):
  car_id: int
  customer_id: int
  agent_id: int
  comments: Optional[str] = None

class SalesTransactionEdit(BaseModel):
  car_id: int
  customer_id: int
  agent_id: int
  comments: Optional[str] = None
