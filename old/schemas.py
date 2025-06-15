from datetime import datetime, date
from decimal import Decimal
from typing import Generic, TypeVar, List, Optional

from pydantic import BaseModel

from models import AccountType, AccountStatus


# Define a generic type variable
T = TypeVar("T")

# Create a generic pagination schema
class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]  # List of items of type T
    total: int  # Total number of items

class LoginRequest(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    firstname: str
    middlename: str
    lastname: str
    email: str
    contact_num: str
    account_type: str
    status: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    firstname: str
    middlename: Optional[str] = None
    lastname: str
    email: str
    contact_num: Optional[str] = None
    password: str
    account_type: AccountType
    status: AccountStatus


class UserEdit(BaseModel):
    firstname: str
    middlename: Optional[str] = None
    lastname: str
    email: str
    contact_num: Optional[str] = None
    password: str
    account_type: AccountType
    status: AccountStatus
    

class SystemLogsResponse(BaseModel):
    id: int
    description: str
    user_id: int
    created_by: str
    created_date: datetime
    user: Optional[UserResponse]  # Nested user schema

    class Config:
        from_attributes = True

# ITEM
class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    created_by: Optional[str]
    created_date: datetime
    updated_by: Optional[str]
    updated_date: datetime

    class Config:
        from_attributes = True

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None

class ItemEdit(BaseModel):
    name: Optional[str]
    description: Optional[str] = None
