from fastapi import Depends, HTTPException
from dependencies import AsyncSessionDep, get_current_active_user, get_password_hash
from models.users import User, AccountStatus, AccountType
from models.system_logs import System_Log
from schemas.users import UserCreate, UserEdit
from sqlalchemy import select, or_
from typing import Annotated, Optional
from sqlalchemy.exc import IntegrityError


async def create_user(
    db: AsyncSessionDep,
    user_create: UserCreate,
    current_user: Annotated[User, Depends(get_current_active_user)] 
):
  new_user = User(
    # Information
    firstname=user_create.firstname.upper(),
    middlename=user_create.middlename.upper(),
    lastname=user_create.lastname.upper(),
    contact_num=user_create.contact_num,
    # Credentials
    email=user_create.email,
    password=get_password_hash(user_create.password),
    # Account details
    type=user_create.type,
    status=user_create.status,
  )
  
  system_log = System_Log(
    action=f"New User {user_create.email} created successfully.",
    user_id=current_user.id
  )
  
  try:
    async with db.begin():
      await db.add_all([
        new_user, 
        system_log
      ])
      await db.commit()
      return {"detail": "User successfully created."}
  except IntegrityError as e:
    await db.rollback()  
    raise HTTPException(status_code=400, detail=f"Database integrity error. {str(e)}")
  except Exception as e:
    await db.rollback()  
    raise HTTPException(status_code=500, detail=f"An unexpected error occurred. {str(e)}")


async def get_users(
  db: AsyncSessionDep,
  current_user: Annotated[User, Depends(get_current_active_user)],
  offset: int = 0,
  limit: int = 10,
  type: Optional[AccountType] = None,
  status: Optional[AccountStatus] = None,
  search: Optional[str] = None
):
  
  query = select(User)
  if type:
      query = query.where(User.type == type)
  if status:
      query = query.where(User.status == status)
  if search:
    query = query.where(
      or_(
        User.firstname.ilike(f"%{search}%"),
        User.middlename.ilike(f"%{search}%"),
        User.lastname.ilike(f"%{search}%"),
        User.email.ilike(f"%{search}%"),
      )
    )
  query = query.offset(offset).limit(limit)
  result = await db.execute(query)
  return result.scalars().all()


async def get_user_by_id(
  id: int,
  db: AsyncSessionDep,
):
  query = select(User).where(User.id == id)
  result = await db.execute(query)
  return result.scalars().first()


async def get_user_by_email(db: AsyncSessionDep, email: str):
  query = select(User).where(User.email == email)
  result = await db.execute(query)
  return result.scalars().first()


async def update_user_by_id(
  id: int,
  db: AsyncSessionDep,
  user_edit: UserEdit,
  current_user: Annotated[User, Depends(get_current_active_user)]
):          
  try:
    async with db.begin():
      user = await get_user_by_id(db, id)
      
      # Information
      user.firstname=user_edit.firstname.upper()
      user.middlename=user_edit.middlename.upper()
      user.lastname=user_edit.lastname.upper()
      user.contact_num=user_edit.contact_num
      # Credentials
      user.email=user_edit.email
      user.password=get_password_hash(user_edit.password)
      # Account details
      user.type=user_edit.type
      user.status=user_edit.status
      
      system_log = System_Log(
        action=f"User {user.email} updated successfully.",
        user_id=current_user.id
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
  