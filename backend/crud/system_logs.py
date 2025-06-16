from typing import Annotated, Optional, cast
from fastapi import Depends, HTTPException
from sqlalchemy import String, or_, select
from backend.dependencies import AsyncSessionDep, get_current_active_user
from backend.models.system_logs import System_Log
from backend.models.users import User
from backend.schemas.system_logs import SystemLogCreate
from sqlalchemy.exc import IntegrityError


async def get_system_logs(
  db: AsyncSessionDep,
  current_user: Annotated[User, Depends(get_current_active_user)],
  offset: int = 0,
  limit: int = 10,
  search: Optional[str] = None,

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