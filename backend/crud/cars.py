from typing import Optional
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy import  delete, or_, select
from models.cars import Car, CarStatus, FuelType, TransmissionType
from models.system_logs import System_Log
from models.users import User
from schemas.cars import CarCreate, CarUpdate
from sqlalchemy.ext.asyncio import AsyncSession



async def create_car(
    db: AsyncSession,
    car_create: CarCreate,
    current_user: User
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
    status = car_create.status,
    
    created_by = current_user.email,
    updated_by = current_user.email
  )
  
  system_log = System_Log(
    action=f"User {current_user.id} created car {car_create.vin}",
    user_id=current_user.id,
  )
  
  try:
    db.add_all([
      new_car, 
      system_log
    ])
    await db.commit()
    return {"detail": f"Car {new_car.vin} {new_car.year} {new_car.make} {new_car.model} created successfully"}
  except IntegrityError as e:
    await db.rollback()  
    raise HTTPException(status_code=400, detail=f"Database integrity error. {str(e)}")
  except Exception as e:
    await db.rollback()  
    raise HTTPException(status_code=500, detail=f"An unexpected error occurred. {str(e)}")


async def read_cars(
  db: AsyncSession,
  current_user: User,
  offset: int = 0,
  limit: int = 10,
  year: Optional[int] = None,
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
  if(year):
    query = query.where(Car.year == year)
    
  if search:
    query = query.where(
      or_(
        Car.make.ilike(f"%{search}%"),
        Car.model.ilike(f"%{search}%"),
        Car.color.ilike(f"%{search}%"),
      )
    )
    
  query = query.offset(offset).limit(limit)
  result = await db.execute(query)
  return result.scalars().all()


async def read_car_by_id(
  id: int,
  db: AsyncSession,
):
  query = select(Car).where(Car.id == id)
  result = await db.execute(query)
  return result.scalars().first()


async def read_car_by_vin(
  vin: str,
  db: AsyncSession,
):
  query = select(Car).where(Car.vin == vin)
  result = await db.execute(query)
  return result.scalars().first()


async def update_car_by_id(
  id: int,
  db: AsyncSession,
  car_edit: CarUpdate,
  current_user: User
):
            
  try:
    car = await read_car_by_id(id=id, db=db)

    car.vin = car_edit.vin
    car.make = car_edit.make.upper()
    car.model = car_edit.model.upper()
    car.year = car_edit.year
    car.color = car_edit.color.upper()
    car.mileage = car_edit.mileage
    car.price = car_edit.price
    car.transmission_type = car_edit.transmission_type
    car.fuel_type = car_edit.fuel_type
    car.status = car_edit.status
    
    
    car.updated_by = current_user.email
    
    
    system_log = System_Log(
      action=f"User {current_user.id} updated car {car.vin}",
      user_id=current_user.id,
    )
    
    db.add(system_log)
    await db.commit()
    return {"detail": f"Car {car.vin} {car.year} {car.make} {car.model} updated successfully"}
  except IntegrityError as e:
    await db.rollback()  
    raise HTTPException(status_code=400, detail=f"Database integrity error. {str(e)}")
  except Exception as e:
    await db.rollback() 
    raise HTTPException(status_code=500, detail=f"An unexpected error occurred. {str(e)}")
    

async def delete_car(
  id: int,
  db: AsyncSession,
  current_user: User
): 
  try:
    # Fetch the car first to log the info and check existence
    car = await read_car_by_id(id=id, db=db)
    if not car:
      raise HTTPException(status_code=404, detail="Car not found")

    # Create a log before deleting
    system_log = System_Log(
      action=f"User {current_user.id} deleted car {car.vin}",
      user_id=current_user.id,
    )

    # Delete the car
    query = delete(Car).where(Car.id == id)
    await db.execute(query)
    db.add(system_log)
    await db.commit()
    
    return {"detail": f"Car {car.vin} {car.year} {car.make} {car.model} deleted successfully"}

  except Exception as e:
    await db.rollback()
    raise HTTPException(status_code=500, detail=f"An unexpected error occurred. {str(e)}")
