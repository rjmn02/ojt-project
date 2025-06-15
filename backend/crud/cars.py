from typing import List, Optional
from fastapi import HTTPException
from pymysql import IntegrityError
from sqlalchemy import String, cast, or_, select
from backend.dependencies import AsyncSessionDep
from backend.models.cars import Car, CarStatus, FuelType, TransmissionType
from backend.models.system_logs import System_Log
from backend.schemas.cars import CarCreate, CarEdit


async def create_car(
    db: AsyncSessionDep,
    car_create: CarCreate,
    current_user
):
  new_car = Car(
    vin = car_create.vin,
    make = car_create.make.upper(),
    model = car_create.model.upper(),
    year = car_create.year,
    color = car_create.color.upper(),
    mileage = car_create.mileage,
    price = car_create.price,
    transmission_type = car_create.transmission_type,
    fuel_type = car_create.fuel_type,
    
    created_by = current_user.get("sub")
  )
  
  system_log = System_Log(
    action=f"New Car {car_create.vin} {car_create.year} {car_create.make} {car_create.model} created successfully.",
    user_id=current_user.get("id"),
    created_by=current_user.get("sub"),
  )
  
  try:
    async with db.begin():
      await db.add_all([
        new_car, 
        system_log
      ])
      await db.commit()
      return {"detail": "Car successfully created."}
  except IntegrityError as e:
    await db.rollback()  
    raise HTTPException(status_code=400, detail=f"Database integrity error. {str(e)}")
  except Exception as e:
    await db.rollback()  
    raise HTTPException(status_code=500, detail=f"An unexpected error occurred. {str(e)}")


async def get_cars(
  db: AsyncSessionDep,
  offset: int = 0,
  limit: int = 10,
  transmission_type: Optional[TransmissionType] = None,
  status: Optional[CarStatus] = None,
  fuel_type: Optional[FuelType] = None,
  search: Optional[str] = None
):
  
  query = select(Car)
  if(transmission_type):
    query = query.where(Car.transmission_type == transmission_type)
  if(status):
    query = query.where(Car.status == status)
  if(fuel_type):
    query = query.where(Car.fuel_type == fuel_type)
    
  if search:
    query = query.where(
      or_(
        cast(Car.year, String).ilike(f"%{search}%"),
        Car.make.ilike(f"%{search}%"),
        Car.model.ilike(f"%{search}%"),
        Car.color.ilike(f"%{search}%"),
      )
    )
    
  query = query.offset(offset).limit(limit)
  result = await db.execute(query)
  return result.scalars().all()


async def get_car_by_id(
  id: int,
  db: AsyncSessionDep,
):
  query = select(Car).where(Car.id == id)
  result = await db.execute(query)
  return result.scalars().first()


async def get_car_by_vin(
  vin: str,
  db: AsyncSessionDep,
):
  query = select(Car).where(Car.vin == vin)
  result = await db.execute(query)
  return result.scalars().first()


async def update_car_by_id(
  id: int,
  db: AsyncSessionDep,
  car_edit: CarEdit,
  current_user
):
            
  try:
    async with db.begin():
      car = await get_car_by_id(db, id)
  
      car.vin = car_edit.vin,
      car.make = car_edit.make.upper(),
      car.model = car_edit.model.upper(),
      car.year = car_edit.year,
      car.color = car_edit.color.upper(),
      car.mileage = car_edit.mileage,
      car.price = car_edit.price,
      car.transmission_type = car_edit.transmission_type,
      car.fuel_type = car_edit.fuel_type
      
      car.updated_by = current_user.get("sub")
      
      
      system_log = System_Log(
        action=f"Car {car.vin} {car.year} {car.make} {car.model} updated successfully.",
        user_id=current_user.get("id"),
        created_by=current_user.get("sub"),
      )
      
      await db.add(system_log)
      await db.commit()
      return {"detail": "User successfully updated."}
  except IntegrityError as e:
    await db.rollback()  
    raise HTTPException(status_code=400, detail=f"Database integrity error. {str(e)}")
  except Exception as e:
    await db.rollback() 
    raise HTTPException(status_code=500, detail=f"An unexpected error occurred. {str(e)}")
    
