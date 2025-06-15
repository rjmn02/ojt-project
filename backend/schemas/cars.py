from models.cars import TransmissionType, FuelType, CarStatus
from pydantic import BaseModel
from typing import Optional
from schemas.sales_transactions import SalesTransactionResponse

class CarResponse(BaseModel):
  id: int
  vin: str
  make: str
  model: str
  year: int
  color: str
  mileage: int
  price: int
  transmission_type: str
  fuel_type: str
  status: str

  sales_transactions: Optional[SalesTransactionResponse] = None

  model_config = {
    "from_attributes": True
  }

class CarCreate(BaseModel):
  vin: str
  make: str
  model: str
  year: int
  color: str
  mileage: Optional[int] = None
  price: int
  transmission_type: TransmissionType
  fuel_type: FuelType
  status: CarStatus
  
  created_by: str
  

class CarEdit(BaseModel):
  vin: str
  make: str
  model: str
  year: int
  color: str
  mileage: Optional[int] = None
  price: int
  transmission_type: TransmissionType
  fuel_type: FuelType
  status: CarStatus
  
  updated_by: str