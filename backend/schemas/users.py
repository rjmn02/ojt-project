from typing import Optional
from pydantic import BaseModel
from models import AccountType, AccountStatus
from schemas.sales_transactions import SalesTransactionResponse

class UserResponse(BaseModel):
  id: int
  firstname: str
  middlename: str
  lastname: str
  contact_num: str

  email: str

  type: str
  status: str

  sales_as_customer: Optional[SalesTransactionResponse] = None
  sales_as_agent: Optional[SalesTransactionResponse] = None

  model_config = {
      "from_attributes": True
  }

class UserCreate(BaseModel):
  firstname: str
  middlename: Optional[str] = None
  lastname: str
  contact_num: Optional[str] = None

  email: str
  password: str

  type: AccountType
  status: AccountStatus


class UserEdit(BaseModel):
  firstname: str
  middlename: Optional[str] = None
  lastname: str
  contact_num: Optional[str] = None

  email: str
  password: str

  type: AccountType
  status: AccountStatus
  

