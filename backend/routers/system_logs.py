from typing import Annotated, List, Optional
from fastapi import  APIRouter, Depends
from crud.system_logs import read_system_logs
from dependencies import AsyncSessionDep, get_current_active_user
from models.users import User
from schemas.system_logs import SystemLogsResponse


router = APIRouter(
  prefix="/api/system_logs",
  tags=["system_logs"],
  dependencies=[
    Depends(get_current_active_user)
  ]
)

@router.get("", response_model = List[SystemLogsResponse])
async def get_system_logs(
  db: AsyncSessionDep,
  current_user:  Annotated[User, Depends(get_current_active_user)],
  page: int = 0,
  page_size: int = 10,
  search: Optional[str] = None
):
  return await read_system_logs(
    db=db,
    current_user=current_user,
    offset=page,
    limit=page_size,
    search=search
  )
