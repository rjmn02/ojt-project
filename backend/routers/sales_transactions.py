from typing import Annotated, List, Optional
from fastapi import  APIRouter, Depends
from backend.crud.cars import create_car, read_car_by_id, read_cars, update_car_by_id
from backend.crud.sales_transactions import create_sales_transaction, read_sales_transaction, read_sales_transaction_by_id
from backend.dependencies import AsyncSessionDep, get_current_active_user
from backend.models.cars import CarStatus, FuelType, TransmissionType
from backend.models.users import User
from backend.schemas.cars import CarCreate, CarEdit, CarResponse
from backend.schemas.sales_transactions import SalesTransactionCreate, SalesTransactionEdit, SalesTransactionResponse
from backend.schemas.users import UserResponse


router = APIRouter(
  prefix="/api/sales_transaction",
  tags=["sales_transaction"],
  dependencies=[
    Depends(get_current_active_user)
  ]
)

@router.get("", response_model = List[SalesTransactionResponse])
async def get_sales_transactions(
  db: AsyncSessionDep,
  current_user: Annotated[User, Depends(get_current_active_user)],
  page: int = 0,
  page_size: int = 10
):
  return await read_sales_transaction(
    db=db,
    current_user=current_user,
    offset=page,
    limit=page_size
  ) 


@router.get("/{id}", response_model=SalesTransactionResponse)
async def get_sales_transaction_by_id(
  id: int,
  db: AsyncSessionDep,
):
  return await read_sales_transaction_by_id(
    id=id,
    db=db,
  )


@router.post("", response_model = dict)
async def post_sales_transaction(
  db: AsyncSessionDep,
  sales_transaction_create: SalesTransactionCreate,
  current_user: Annotated[User, Depends(get_current_active_user)]
):
  return await create_sales_transaction(
    db=db,
    sales_transaction_create=sales_transaction_create,
    current_user=current_user
  )


@router.put('/{id}', response_model = dict)
async def put_sales_transaction(
  id: int,
  db: AsyncSessionDep,
  sales_transaction_edit: SalesTransactionEdit,
  current_user: Annotated[User, Depends(get_current_active_user)]
):
  
  return await update_car_by_id(
    id=id,
    db=db,
    sales_transaction_edit=sales_transaction_edit,
    current_user=current_user
  )
