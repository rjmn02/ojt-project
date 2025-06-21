from typing import Optional
from sqlalchemy import  or_, select
from models.system_logs import System_Log
from models.users import User
from sqlalchemy.ext.asyncio import AsyncSession


async def read_system_logs(
  db: AsyncSession,
  current_user: User,
  offset: int = 0,
  limit: int = 10,
  search: Optional[str] = None,

):
  query = select(System_Log).order_by(System_Log.id.desc()).offset(offset).limit(limit)
  if search:
    query = query.where(
      or_(
        System_Log.action.ilike(f"%{search}%"),
      )
    )
  result = await db.execute(query)
  return result.scalars().all()