from typing import Annotated, List, Optional
from fastapi import  APIRouter, Depends
from crud.cars import create_car, delete_car, read_car_by_id, read_cars, update_car_by_id
from dependencies import AsyncSessionDep, get_current_active_user
from models.cars import CarStatus, FuelType, TransmissionType
from models.users import User
from schemas.cars import CarCreate, CarUpdate, CarInDB


router = APIRouter(
  prefix="/api/cars",
  tags=["cars"],
  dependencies=[
    Depends(get_current_active_user)
  ]
)

@router.get("", response_model = List[CarInDB])
async def get_cars(
  db: AsyncSessionDep,
  current_user: Annotated[User, Depends(get_current_active_user)],
  page: int = 0,
  page_size: int = 10,
  year: Optional[int] = None,
  transmission_type: Optional[TransmissionType] = None,
  status: Optional[CarStatus] = None,
  fuel_type: Optional[FuelType] = None,
  search: Optional[str] = None
):
  return await read_cars(
    db=db,
    current_user=current_user,
    offset=page,
    limit=page_size,
    year=year,
    transmission_type=transmission_type,
    status=status,
    fuel_type=fuel_type,
    search=search
  )


@router.get("/{id}", response_model=CarInDB)
async def get_car_by_id(
  id: int,
  db: AsyncSessionDep,
):
  return await read_car_by_id(
    id=id,
    db=db,
  )


@router.post("", response_model = dict)
async def post_car(
  db: AsyncSessionDep,
  car_create: CarCreate,
  current_user: Annotated[User, Depends(get_current_active_user)]
):
  return await create_car(
    db=db,
    car_create=car_create,
    current_user=current_user
  )


@router.put('/{id}', response_model = dict)
async def put_car(
  id: int,
  db: AsyncSessionDep,
  car_edit: CarUpdate,
  current_user: Annotated[User, Depends(get_current_active_user)]
):
  
  return await update_car_by_id(
    id=id,
    db=db,
    car_edit=car_edit,
    current_user=current_user
  )
  
@router.delete('/{id}', response_model = dict)
async def delete_car_route(
  id: int,
  db: AsyncSessionDep,
  current_user: Annotated[User, Depends(get_current_active_user)]
):
  
  return await delete_car(
    id=id,
    db=db,
    current_user=current_user
  )
