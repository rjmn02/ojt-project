from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import engine
from models.base import Base  # ADDED IMPORT
from models import cars, sales_transactions, system_logs, users 

# The first part of the function, before the yield, will be executed before the application starts.
# And the part after the yield will be executed after the application has finished.
@asynccontextmanager
async def lifespan(app: FastAPI):
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
  yield
  await engine.dispose()

app = FastAPI(lifespan=lifespan)



@app.get('/')
async def ping():
  return {'Success': '589725'}