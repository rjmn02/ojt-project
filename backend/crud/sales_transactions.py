

from fastapi import HTTPException
from sqlalchemy import select
from models.sales_transactions import Sales_Transaction
from models.system_logs import System_Log
from models.users import User
from schemas.sales_transactions import SalesTransactionCreate, SalesTransactionUpdate
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

async def create_sales_transaction(
  db: AsyncSession,
  sales_transaction_create: SalesTransactionCreate,
  current_user: User
):
  sales_transaction = Sales_Transaction(
    car_id = sales_transaction_create.car_id,
    customer_id = sales_transaction_create.customer_id,
    agent_id = sales_transaction_create.agent_id,
    comments = sales_transaction_create.comments,
    
    created_by = current_user.email,
    updated_by = current_user.email
  )
  
  system_log = System_Log(
    action=f"Agent User ID {sales_transaction_create.agent_id} sold Car ID {sales_transaction_create.car_id} to Customer ID {sales_transaction_create.customer_id}",
    user_id=current_user.id,
  )
  
  try:
    db.add_all([
      sales_transaction, 
      system_log
    ])
    await db.commit()
    return {"detail": f"Sales transaction successfully created."}
  except IntegrityError as e:
    await db.rollback()  
    raise HTTPException(status_code=400, detail=f"Database integrity error. {str(e)}")
  except Exception as e:
    await db.rollback()
    raise HTTPException(status_code=500, detail=f"An unexpected error occurred. {str(e)}")
    

async def read_sales_transaction(
  db: AsyncSession,
  current_user: User,
  offset: int = 0,
  limit: int = 10
):
  query = select(Sales_Transaction)
  
  query = query.offset(offset).limit(limit)
  result = await db.execute(query)
  return result.scalars().all()


async def read_sales_transaction_by_id(
  id: int,
  db: AsyncSession,
):
  query = select(Sales_Transaction).where(Sales_Transaction.id == id)
  
  result = await db.execute(query)
  return result.scalars().first()



async def update_sales_transaction_by_id(
  id: int,
  db: AsyncSession,
  sales_transaction_edit: SalesTransactionUpdate,
  current_user: User
):
            
  try:
    sales_transaction = await read_sales_transaction_by_id(id=id, db=db)

    sales_transaction.car_id = sales_transaction_edit.car_id
    sales_transaction.customer_id = sales_transaction_edit.customer_id
    sales_transaction.agent_id = sales_transaction_edit.agent_id
    sales_transaction.comments = sales_transaction_edit.comments
    sales_transaction.updated_by = current_user.email
    
    
    system_log = System_Log(
      action=f"Sales Transaction ID {sales_transaction.id} updated by {current_user.email}" ,
      user_id=current_user.id,
    )
    
    db.add(system_log)
    await db.commit()
    return {"detail": f"Sales transaction successfully updated."}
  except IntegrityError as e:
    await db.rollback()  
    raise HTTPException(status_code=400, detail=f"Database integrity error. {str(e)}")
  except Exception as e:
    await db.rollback() 
    raise HTTPException(status_code=500, detail=f"An unexpected error occurred. {str(e)}")
    