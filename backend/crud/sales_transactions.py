from typing import Annotated

from fastapi import Depends, HTTPException
from sqlalchemy import select
from backend.dependencies import AsyncSessionDep, get_current_active_user
from backend.models.sales_transactions import Sales_Transaction
from backend.models.system_logs import System_Log
from backend.models.users import User
from backend.schemas.sales_transactions import SalesTransactionCreate, SalesTransactionEdit
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

async def create_sales_transaction(
  db: AsyncSessionDep,
  sales_transaction_create: SalesTransactionCreate,
  current_user: Annotated[User, Depends(get_current_active_user)] 

):
  sales_transaction = Sales_Transaction(
    car_id = sales_transaction_create.car_id,
    customer_id = sales_transaction_create.customer_id,
    agent_id = sales_transaction_create.agent_id,
    comments = sales_transaction_create.comments
  )
  
  system_log = System_Log(
    action=f"Agent User ID {sales_transaction_create.agent_id} sold Car ID {sales_transaction_create.car_id} to Customer ID {sales_transaction_create.customer_id}",
    user_id=current_user.id,
  )
  
  try:
    async with db.begin():
      await db.add_all([
        sales_transaction, 
        system_log
      ])
      await db.commit()
      return {"detail": "Sales transaction successfully created."}
  except IntegrityError as e:
    await db.rollback()  
    raise HTTPException(status_code=400, detail=f"Database integrity error. {str(e)}")
  except Exception as e:
    await db.rollback()  
    


async def get_sales_transaction(
  db: AsyncSessionDep,
  current_user: Annotated[User, Depends(get_current_active_user)],
  offset: int = 0,
  limit: int = 10
):
  query = select(Sales_Transaction).options(
    joinedload(Sales_Transaction.car),
    joinedload(Sales_Transaction.customer),
    joinedload(Sales_Transaction.agent)
  ).offset(offset).limit(limit)
  
  result = await db.execute(query)
  return result.scalars().all()

async def get_sales_transaction_by_id(
  id: int,
  db: AsyncSessionDep,
):
  query = select(Sales_Transaction).options(
    joinedload(Sales_Transaction.car),
    joinedload(Sales_Transaction.customer),
    joinedload(Sales_Transaction.agent)
  ).where(Sales_Transaction.id == id)
  
  result = await db.execute(query)
  return result.scalars().first()



async def update_sales_transaction_by_id(
  id: int,
  db: AsyncSessionDep,
  sales_transaction_edit: SalesTransactionEdit,
  current_user: Annotated[User, Depends(get_current_active_user)],
):
            
  try:
    async with db.begin():
      sales_transaction = await get_sales_transaction_by_id(db, id)
  
      sales_transaction.car_id = sales_transaction_edit.car_id
      sales_transaction.customer_id = sales_transaction_edit.customer_id
      sales_transaction.agent_id = sales_transaction_edit.agent_id
      sales_transaction.comments = sales_transaction_edit.comments
      
      
      system_log = System_Log(
        action=f"Sales Transaction ID {sales_transaction.id} updated by {current_user.email}" ,
        user_id=current_user.id,
      )
      
      await db.add(system_log)
      await db.commit()
      return {"detail": "Sales transaction successfully updated."}
  except IntegrityError as e:
    await db.rollback()  
    raise HTTPException(status_code=400, detail=f"Database integrity error. {str(e)}")
  except Exception as e:
    await db.rollback() 
    raise HTTPException(status_code=500, detail=f"An unexpected error occurred. {str(e)}")
    