
from datetime import timedelta
from fastapi import  APIRouter, HTTPException, status
from dependencies import ACCESS_TOKEN_EXPIRE_MINUTES, AsyncSessionDep, authenticate_user, create_access_token
from schemas.login import LoginRequest
from schemas.tokens import Token


router = APIRouter()

@router.post("/api/login")
async def login_for_access_token(
  login: LoginRequest,
  db: AsyncSessionDep
) -> Token:
  # Use the async session and authenticate with email
  user = await authenticate_user(db, login.email, login.password)
  if not user:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect email or password",
      headers={"WWW-Authenticate": "Bearer"},
    )
  
  access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(
    data={"sub": user.email},  # Use email as the subject
    expires_delta=access_token_expires
  )
  
  return Token(access_token=access_token, token_type="bearer")

