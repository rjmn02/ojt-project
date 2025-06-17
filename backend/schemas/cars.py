from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from typing import Any, Optional

class TransmissionType(str, Enum):
  MANUAL = "MANUAL"
  AUTOMATIC = "AUTOMATIC"

class FuelType(str, Enum):
  PETROL = "PETROL"
  DIESEL = "DIESEL"
  ELECTRIC = "ELECTRIC"
  HYBRID = "HYBRID"

class CarStatus(str, Enum):
  AVAILABLE = "AVAILABLE"
  SOLD = "SOLD"
  RESERVED = "RESERVED"


class CarBase(BaseModel):
  vin: str
  year: int
  make: str
  model: str
  color: str
  mileage: int
  price: int
  transmission_type: TransmissionType
  fuel_type: FuelType
  status: CarStatus = CarStatus.AVAILABLE

class CarCreate(CarBase):
  created_by: str

class CarUpdate(CarBase):
  vin: Optional[str] = None
  year: Optional[int] = None
  make: Optional[str] = None
  model: Optional[str] = None
  color: Optional[str] = None
  mileage: Optional[int] = None
  price: Optional[int] = None
  transmission_type: Optional[TransmissionType] = None
  fuel_type: Optional[FuelType] = None
  status: Optional[CarStatus] = None
  
  updated_by: str

class CarInDB(CarBase):
  id: int
  created_at: datetime
  updated_at: datetime
  created_by: str
  updated_by: str
  
  sale_transaction: Optional[Any]

  model_config = {
    "from_attributes": True
  }