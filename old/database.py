from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Async database URL for MySQL
DATABASE_URL = "mysql+aiomysql://root:rootpass@localhost/dbgoldenvillemgtsystem"


# Async SQLAlchemy engine and session setup
engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Dependency to get async database session
async def get_db():
    async with async_session() as session:
        yield session