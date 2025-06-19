
from datetime import timedelta
from fastapi import  APIRouter, HTTPException, Response
from sqlalchemy import select
from crud.users import create_user
from models.users import User
from models.system_logs import System_Log
from dependencies import ACCESS_TOKEN_EXPIRE_MINUTES, AsyncSessionDep, authenticate_user, create_access_token, get_password_hash
from schemas.auth import LoginRequest, Register
from schemas.tokens import Token
from sqlalchemy.exc import IntegrityError
  


router = APIRouter()


router = APIRouter(
  prefix="/auth",
  tags=["auth"],
)

@router.post("/login")
async def login_for_access_token(
  response: Response,
  login: LoginRequest,
  db: AsyncSessionDep
) -> dict:
  
  try:
    async with db.begin():
          # Use the async session and authenticate with email
      user = await authenticate_user(db, login.email, login.password)
      if not user:
        raise HTTPException(
          status_code=400,
          detail="Incorrect email or password",
          headers={"WWW-Authenticate": "Bearer"},
        )
      
      access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
      access_token = create_access_token(
        data={
          "sub": user.email,
          "user_type": user.type.value   # Convert enum to string value
          },  # Use email as the subject
        expires_delta=access_token_expires
      )
      
      system_log = System_Log(
        action=f"User {user.email} Logged in.",
        user_id=user.id
      )
      
      db.add(system_log)
      await db.commit()
      
      response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,  # Prevents JavaScript access
        # PRODUCTION
        #samesite="lax", 
        #secure=True, 
        
        # DEV
        samesite="none", 
        secure=True,    
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60  # Convert minutes to seconds
      )
      
      return {"detail": "Successfully logged in"}

  except IntegrityError as e:
    await db.rollback()  
    raise HTTPException(status_code=400, detail=f"Database integrity error. {str(e)}")
  except Exception as e:
    await db.rollback()  
    raise HTTPException(status_code=500, detail=f"An unexpected error occurred. {str(e)}")



@router.post('/register')
async def register_user(
  register: Register,
  db: AsyncSessionDep
):
  new_user = User(
    # Information
    firstname=register.firstname.upper(),
    middlename=register.middlename.upper() if register.middlename else None,
    lastname=register.lastname.upper(),
    contact_num=register.contact_num if register.contact_num else None,
    # Credentials
    email=register.email,
    password=get_password_hash(register.password),
    # Account details
    type=register.type,
  )
  
  system_log = System_Log(
    action=f"User {register.email} registered successfully.",
    user_id=0
  )
  check_existing_user_query = select(User).filter(User.email == register.email)
  try:
    async with db.begin():
      
      result = await db.execute(check_existing_user_query)
      existing_user = result.scalar_one_or_none()
      if existing_user:
        raise HTTPException(
          status_code=400,
          detail="Email already registered"
        )
      db.add(new_user)
      await db.flush()
      
      system_log = System_Log(
        action=f"User {new_user.email} registered successfully.",
        user_id=new_user.id
      )
      db.add(system_log)
      await db.commit()
      return {"detail": f"User successfully created."}
  except IntegrityError as e:
    await db.rollback()  
    raise HTTPException(status_code=400, detail=f"Database integrity error. {str(e)}")
  except Exception as e:
    await db.rollback()  
    raise HTTPException(status_code=500, detail=f"An unexpected error occurred. {str(e)}")
  
  
@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"detail": "Successfully logged out"}