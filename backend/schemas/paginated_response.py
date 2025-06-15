
from typing import Generic, TypeVar, List

from pydantic import BaseModel



T = TypeVar("T")

# Create a generic pagination schema
class PaginatedResponse(BaseModel, Generic[T]):
    data: List[T]  # List of items of type T
    total: int  # Total number of items