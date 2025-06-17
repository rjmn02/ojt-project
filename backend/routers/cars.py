from typing import Annotated, List, Optional
from fastapi import  APIRouter, Depends
from backend.crud.cars import create_car, read_car_by_id, read_cars, update_car_by_id
from backend.dependencies import AsyncSessionDep, get_current_active_user
from backend.models.cars import CarStatus, FuelType, TransmissionType
from backend.models.users import User
from backend.schemas.cars import CarCreate, CarEdit, CarResponse
from backend.schemas.users import UserResponse


router = APIRouter(
  prefix="/api/cars",
  tags=["cars"],
  dependencies=[
    Depends(get_current_active_user)
  ]
)

@router.get("", response_model = List[CarResponse])
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


@router.get("/{id}", response_model=CarResponse)
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
  car_edit: CarEdit,
  current_user: Annotated[User, Depends(get_current_active_user)]
):
  
  return await update_car_by_id(
    id=id,
    db=db,
    car_edit=car_edit,
    current_user=current_user
  )
