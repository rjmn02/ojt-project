from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from fastapi import Depends, HTTPException, status
from models.users import AccountStatus, AccountType
from schemas.tokens import TokenData
from database import get_session
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi.security import APIKeyCookie
from models.users import User
import jwt
import os
from dotenv import load_dotenv
from jwt.exceptions import InvalidTokenError
from sqlalchemy import select

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# ASYNC DB SESSION
AsyncSessionDep = Annotated[AsyncSession, Depends(get_session)]

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
cookie_scheme = APIKeyCookie(name="access_token", auto_error=True)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def authenticate_user(db: AsyncSessionDep, email: str, password: str):
    user = await read_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

async def read_user_by_email(db: AsyncSessionDep, email: str):
  query = select(User).where(User.email == email)
  result = await db.execute(query)
  return result.scalars().first()

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(cookie_scheme)],
    db: AsyncSessionDep,
):
    """Validate the JWT token and fetch the current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception

    user = await read_user_by_email(db=db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Ensure the current user is active."""
    if current_user.status != AccountStatus.ACTIVE:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user