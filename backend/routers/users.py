from typing import Annotated, List, Optional
from fastapi import  APIRouter, Depends
from crud.users import create_user, read_user_by_id, read_users, update_user_by_id
from dependencies import AsyncSessionDep, get_current_active_user
from models.users import AccountStatus, AccountType, User
from schemas.users import UserCreate, UserUpdate, UserInDB


router = APIRouter(
  prefix="/api/users",
  tags=["users"],
  dependencies=[
    Depends(get_current_active_user)
  ]
)

@router.get("", response_model = List[UserInDB])
async def get_users(
  db: AsyncSessionDep,
  current_user: Annotated[User, Depends(get_current_active_user)],
  page: int = 0,
  page_size: int = 10,
  type: Optional[AccountType] = None,
  status: Optional[AccountStatus] = None,
  search: Optional[str] = None
):
  return await read_users(
    db=db,
    current_user=current_user,
    offset=page,
    limit=page_size,
    type=type,
    status=status,
    search=search
  )


@router.get("/{id}", response_model=UserInDB)
async def get_user_by_id(
  id: int,
  db: AsyncSessionDep,
):
  return await read_user_by_id(
    id=id,
    db=db,
  )

@router.post("", response_model = dict)
async def post_user(
  db: AsyncSessionDep,
  current_user: Annotated[User, Depends(get_current_active_user)],
  user_create: UserCreate
):
  return await create_user(
    db=db,
    current_user=current_user,
    user_create=user_create
  )


@router.put('/{id}',response_model = dict)
async def put_user(
  id: int,
  db: AsyncSessionDep,
  current_user: Annotated[User, Depends(get_current_active_user)],
  user_edit: UserUpdate
):
  
  return await update_user_by_id(
    id=id,
    db=db,
    current_user=current_user,
    user_edit=user_edit
  )
