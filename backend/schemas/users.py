from datetime import datetime
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel
class AccountType(str, Enum):
  ADMIN = "ADMIN"
  AGENT = "AGENT"
  CLIENT = "CLIENT"
  
class AccountStatus (str, Enum):
  ACTIVE = "ACTIVE"
  INACTIVE = "INACTIVE"

class UserBase(BaseModel):
  email: str
  
  firstname: str
  middlename: str
  lastname: str
  contact_num: str

  type: AccountType
  status: AccountStatus
  
class UserCreate(UserBase):
  password: str
  created_by: str

class UserUpdate(UserBase):
  email: str
  
  firstname: str
  middlename: Optional[str] = None
  lastname: str
  contact_num: str

  type: AccountType
  status: AccountStatus

class UserInDB(UserBase):
  id: int
  created_at: datetime
  updated_at: datetime

  logs: Optional[Any] = None
  sales_as_customer: Optional[Any] = None
  sales_as_agent: Optional[Any] = None
  
  model_config = {
    "from_attributes": True
  }

