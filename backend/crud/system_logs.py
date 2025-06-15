from typing import Optional, cast
from sqlalchemy import String, or_, select
from backend.dependencies import AsyncSessionDep
from backend.models.system_logs import System_Log


async def get_system_logs(
  db: AsyncSessionDep,
  offset: int = 0,
  limit: int = 10,
  search: Optional[str] = None
):
  query = select(System_Log).offset(offset).limit(limit)
  if search:
    query = query.where(
      or_(
        System_Log.action.ilike(f"%{search}%"),
      )
    )
  result = await db.execute(query)
  return result.scalars().all()