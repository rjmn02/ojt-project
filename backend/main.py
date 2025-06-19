from fastapi import FastAPI, Cookie
from contextlib import asynccontextmanager

from sqlalchemy import select
from database import engine
from models.base import Base  # ADDED IMPORT
from routers import cars, auth, sales_transactions, system_logs, users
from fastapi.middleware.cors import CORSMiddleware

# The first part of the function, before the yield, will be executed before the application starts.
# And the part after the yield will be executed after the application has finished.
@asynccontextmanager
async def lifespan(app: FastAPI):
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
    
  await initialize_admin_user()
  yield
  await engine.dispose()

app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(cars.router)
app.include_router(sales_transactions.router)
app.include_router(system_logs.router)


from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from dependencies import get_password_hash
from models.users import User, AccountType, AccountStatus

async def initialize_admin_user():
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)

  async with AsyncSession(engine) as db:
    admin_email = "techguru@gmail.com"
    result = await db.execute(select(User).where(User.email == admin_email))
    admin_user = result.scalars().first()
    
    if not admin_user:
      hashed_password = get_password_hash("techguruadmin01")
      admin_user = User(
          firstname="TECH",
          middlename="",
          lastname="GURU",
          email=admin_email,
          contact_num="00000000000",
          password=hashed_password,
          type=AccountType.ADMIN,
          status=AccountStatus.ACTIVE
      )
      db.add(admin_user)

      await db.commit()
      print("Admin user initialized successfully")
    else:
      print("Admin user already exists")