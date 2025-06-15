from typing import Optional
from pydantic import BaseModel

from backend.models.users import AccountType

class LoginRequest(BaseModel):
    email: str
    password: str
    
    
class Register(BaseModel):
  firstname: str
  middlename: Optional[str] = None
  lastname: str
  contact_num: Optional[str] = None

  email: str
  password: str

  type: AccountType