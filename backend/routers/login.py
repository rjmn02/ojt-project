
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, FastAPI, HTTPException, status
from typing import Annotated, Union
from backend.dependencies import ACCESS_TOKEN_EXPIRE_MINUTES, AsyncSessionDep, authenticate_user, create_access_token
from backend.schemas.tokens import Token


app = FastAPI()

@app.post("/token")
async def login_for_access_token(
  form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
  db: AsyncSessionDep
) -> Token:
  # Use the async session and authenticate with email
  user = await authenticate_user(db, form_data.username, form_data.password)
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

