from datetime import timedelta, datetime
from typing import AsyncGenerator

import socketio
from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from socketio import AsyncServer
from sqlalchemy import select, or_, and_, not_, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database import get_db, Base, engine
from models import User, System_logs, Item
from schemas import UserResponse, UserCreate, UserEdit, SystemLogsResponse, LoginRequest, \
    PaginatedResponse, \
    ItemResponse, ItemEdit, ItemCreate

# Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Configuration
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

# Password hashing utility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Initialize FastAPI app
async def lifespan(app: FastAPI) -> AsyncGenerator:
    # Startup logic
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)
    await initialize_admin_user()

    yield  # App is now running

    # Shutdown logic

    await engine.dispose()  # Closes all connections in the connection pool
    print("Database engine disposed. Resources have been cleaned up.")


app = FastAPI(lifespan=lifespan)

sio = AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",
    # client_manager=AsyncRedisManager("redis://localhost:6379"),
    ping_timeout=30,  # Adjust timeout
    ping_interval=25,
)

app.mount("/socket.io", socketio.ASGIApp(sio, other_asgi_app=app))

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies and credentials
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Utility functions
def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now() + (expires_delta or timedelta(days=1))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# WebSocket for a unique room
@sio.on("connect")
async def connect_handler(sid, environ):
    print(f"Client connected: {sid}")


@sio.on("join_room")
async def join_room_handler(sid, data):
    room_name = data.get("room")
    await sio.enter_room(sid, room_name)
    print(f"Client {sid} joined room {room_name}")


@sio.on("leave_room")
async def leave_room_handler(sid, data):
    room_name = data.get("room")
    if room_name:
        await sio.leave_room(sid, room_name)
        print(f"Client {sid} left room {room_name}")
    else:
        print(f"Client {sid} tried to leave a room without specifying a room name.")


@sio.on("disconnect")
async def disconnect_handler(sid):
    print(f"Client disconnected: {sid}")


# Dependency to validate token
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if user_email is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No user with this email address found.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return payload  # Return the decoded token payload (e.g., user_email, account_type)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def initialize_admin_user():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as db:
        admin_email = "techguru@gmail.com"
        result = await db.execute(User.__table__.select().where(User.email == admin_email))
        admin_user = result.scalars().first()
        if not admin_user:
            created_date_now = datetime.now()
            hashed_password = get_password_hash("techguruadmin01")
            admin_user = User(
                firstname="Tech",
                middlename="",
                lastname="Guru",
                email=admin_email,
                contact_num="00000000",
                password=hashed_password,
                account_type="SUPER_ADMIN",
            )
            db.add(admin_user)

            await db.commit()
            print("Initialized Successfully")
        else:
            print("No need to initialize")


@app.post("/api/login")
async def login_for_access_token(login_request: LoginRequest, db: AsyncSession = Depends(get_db)):
    created_date_now = datetime.now()
    # Use select() instead of query()
    stmt = select(User).where(
        and_(
            func.lower(User.email) == login_request.email.lower(),
            User.status == "ACTIVE"
        )
    )
    result = await db.execute(stmt)
    user = result.scalars().first()  # Extract the first result as a User object

    if not user or not verify_password(login_request.password, user.password):
        if not user:
            raise HTTPException(status_code=404, detail="User not found or not yet verified")
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")

    # Create an access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "account_type": str(user.account_type), "id": user.id},
        expires_delta=access_token_expires
    )

    # Add a system log for user login
    system_log = System_logs(
        description=f"User {user.email} logged in successfully.",
        user_id=user.id,
        created_by=user.email,
        created_date=created_date_now
    )
    db.add(system_log)
    await db.commit()

    return {"access_token": access_token, "token_type": "bearer", "detail": "Logged in successfully"}


@app.get("/api/system-logs", response_model=PaginatedResponse[SystemLogsResponse])
async def get_system_logs(
        page: int = Query(1, ge=1),
        page_size: int = Query(10, ge=1, le=50),
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    offset = (page - 1) * page_size

    # Fetch logs with related user data
    stmt = (
        select(System_logs)
        .options(joinedload(System_logs.user))  # Eagerly load the related User
        # .where(not_(System_logs.user_id == 1))  # Exclude user with id 1
        .offset(offset)
        .limit(page_size)
        .order_by(System_logs.id.desc())
    )
    result = await db.execute(stmt)
    logs = result.scalars().all()

    # Serialize logs into the Pydantic schema
    serialized_logs = [SystemLogsResponse.model_validate(log) for log in logs]

    # Fetch total count for pagination
    total_count_stmt = select(System_logs.id).where(not_(System_logs.user_id == 1))
    total_result = await db.execute(total_count_stmt)
    total = len(total_result.scalars().all())

    return PaginatedResponse(data=serialized_logs, total=total)


@app.get("/api/users", response_model=PaginatedResponse[UserResponse])
async def get_users(
        page: int = Query(1, ge=1),  # Default page is 1, must be >= 1
        page_size: int = Query(10, ge=1, le=50),  # Default page size is 10, max is 50
        search: str = Query("", description="Search term for filtering users"),  # Optional search query
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    offset = (page - 1) * page_size

    # Build the query with search filtering
    stmt = select(User).where(not_(User.id == 1), not_(User.account_type == "BETTER")).offset(offset).limit(
        page_size).order_by(User.firstname.asc())

    if search.strip():  # Apply search if search term is provided
        search_words = search.split(" ")

        search_filters = [
            or_(
                User.firstname.ilike(f"%{word.strip()}%"),
                User.lastname.ilike(f"%{word.strip()}%"),
                User.email.ilike(f"%{word.strip()}%"),
                User.account_type.ilike(f"%{word.strip()}%"),
            )
            for word in search_words if word.strip()
        ]

        if search_filters:
            stmt = stmt.where(or_(*search_filters))

    # Execute the query to fetch users
    result = await db.execute(stmt)
    users = result.scalars().all()

    # Fetch the total count for pagination
    total_stmt = select(func.count(User.id)).where(not_(User.id == 1))  # Efficient way to count rows
    if search.strip():
        total_stmt = total_stmt.where(or_(*search_filters))

    total_result = await db.execute(total_stmt)
    total = total_result.scalar()  # Get the count as a scalar value

    # Serialize the users
    serialized_users = [UserResponse.model_validate(user) for user in users]

    return PaginatedResponse(data=serialized_users, total=total)


@app.post("/api/create-user")
async def add_user(
        user: UserCreate,
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(get_current_user),
):
    try:
        async with db.begin():  # Use a transaction block
            created_date_now = datetime.now()
            # Check if the email already exists
            existing_user = await db.execute(
                select(User).where(func.lower(User.email) == user.email.lower())
            )
            if existing_user.scalars().first():
                raise HTTPException(
                    status_code=400, detail="A user with this email already exists."
                )

            # Create a new User object
            new_user = User(
                # Information
                firstname=user.firstname.upper(),
                middlename=user.middlename.upper(),
                lastname=user.lastname.upper(),
                contact_num=user.contact_num,

                # Credentials
                email=user.email.upper(),
                password=get_password_hash(user.password),

                # Account details
                account_type=user.account_type,
                status=user.status,

                # Audit fields
                created_by=current_user.get("sub"),
                created_date=created_date_now
            )
            db.add(new_user)
            await db.flush()  # Ensures new_user.id is generated before proceeding

            # Log the action in system logs
            system_log = System_logs(
                description=f"New User {user.email} created successfully.",
                user_id=current_user.get("id"),
                created_by=current_user.get("sub"),
                created_date=created_date_now
            )
            db.add(system_log)

        # Commit the transaction (automatically done if no errors occur in the block)

        return {"detail": "User successfully created."}

    except IntegrityError as e:
        # Handle integrity errors (e.g., unique constraint violations)
        await db.rollback()  # Explicit rollback if the transaction block was exited early
        raise HTTPException(status_code=400, detail=f"Database integrity error. {str(e)}")
    except Exception as e:
        await db.rollback()  # Rollback for other exceptions
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred. {str(e)}")


@app.put("/api/update-user/{id}")
async def update_user(
        id: int,
        user_edit: UserEdit,
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(get_current_user)  # Validate token
):
    try:
        # Use a transaction block
        async with db.begin():
            created_date_now = datetime.now()
            # Fetch the user to update
            result = await db.execute(select(User).where(User.id == id))
            user = result.scalars().first()

            if not user:
                raise HTTPException(status_code=404, detail="User not found.")

            # Information 
            user.firstname = user_edit.firstname.upper()
            user.middlename = user_edit.middlename.upper()
            user.lastname = user_edit.lastname.upper()
            user.contact_num = user_edit.contact_num

            # Credentials
            user.email = user_edit.email
            if user_edit.password:
                user.password = get_password_hash(user_edit.password)

            # Account details
            user.account_type = user_edit.account_type
            user.status = user_edit.status
            # Audit fields
            user.updated_by = current_user.get("sub")
            user.updated_date = created_date_now

            # Log the update action
            system_log = System_logs(
                description=f"User {user.email} updated successfully.",
                user_id=current_user.get("id"),
                created_by=current_user.get("sub"),
                created_date=created_date_now
            )
            db.add(system_log)

            # No explicit commit is needed; changes are committed if no exceptions occur

        return {"detail": "User successfully updated."}
    except IntegrityError as e:
        # Handle integrity errors (e.g., unique constraint violations)
        await db.rollback()  # Explicit rollback if the transaction block was exited early
        raise HTTPException(status_code=400, detail=f"Database integrity error. {str(e)}")

    except Exception as e:
        # Rollback the transaction if an exception occurs
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred. {str(e)}")
    
@app.delete("/api/delete-user/{id}")
async def delete_user(
        id: int,
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(get_current_user)  # Validate token
):
    try:
        async with db.begin():  # Use a transaction block
            # Fetch the user to delete
            result = await db.execute(select(User).where(User.id == id))
            user = result.scalars().first()

            if not user:
                raise HTTPException(status_code=404, detail="User not found.")

            # Delete the user
            await db.delete(user)

            # Log the deletion action
            system_log = System_logs(
                description=f"User {user.email} deleted successfully.",
                user_id=current_user.get("id"),
                created_by=current_user.get("sub"),
                created_date=datetime.now()
            )
            db.add(system_log)

        return {"detail": "User successfully deleted."}
    except Exception as e:
        await db.rollback()


# ITEM ENDPOINTS
@app.get('/api/items')
async def get_items(
        page: int = Query(1, ge=1),  # Default page is 1, must be >= 1
        page_size: int = Query(10, ge=1, le=50),  # Default page size is 10, max is 50
        search: str = Query("", description="Search term for filtering items"),  # Optional search query
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(get_current_user)
):
    offset = (page - 1) * page_size

    stmt = (
        select(Item)
        .offset(offset)
        .limit(page_size)
        .order_by(Item.id.desc())
    )

    if search.strip():  # Apply search if search term is provided
        search_words = search.split(" ")

        search_filters = [
            or_(
                Item.name.ilike(f"%{word.strip()}%"),
                Item.description.ilike(f"%{word.strip()}%"),
            )
            for word in search_words if word.strip()
        ]

        if search_filters:
            stmt = stmt.where(or_(*search_filters))

    # Execute the query to fetch users
    result = await db.execute(stmt)
    items = result.scalars().all()

    # Fetch the total count for pagination
    total_stmt = select(func.count(Item.id))  # Efficient way to count rows
    if search.strip():
        total_stmt = total_stmt.where(or_(*search_filters))

    total_result = await db.execute(total_stmt)
    total = total_result.scalar()  # Get the count as a scalar value

    # Serialize the users
    serialized_items = [ItemResponse.model_validate(item) for item in items]

    return PaginatedResponse(data=serialized_items, total=total)

@app.post('/api/create-item')
async def create_item(
        item: ItemCreate,
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(get_current_user),
):
    try:
        async with db.begin():  # Use a transaction block
            created_date_now = datetime.now()
            # Check if the item  already exists
            existing_item = await db.execute(
                select(Item).where(func.lower(Item.name) == item.name.upper())
            )
            if existing_item.scalars().first():
                raise HTTPException(
                    status_code=400, detail="An item with this name already exists."
                )

            # Create a new Item object
            new_item = Item(
                name = item.name.upper(),
                description = item.description,
                created_by = current_user.get("sub"),
                created_date = created_date_now
            )
            db.add(new_item)
            await db.flush()  # Ensures new_item.id is generated before proceeding

            # Log the action in system logs
            system_log = System_logs(
                description=f"New Item {item.name} created successfully.",
                user_id=current_user.get("id"),
                created_by=current_user.get("sub"),
                created_date=created_date_now
            )
            db.add(system_log)

        # Commit the transaction (automatically done if no errors occur in the block)

        return {"detail": "Item successfully created."}

    except IntegrityError as e:
        # Handle integrity errors (e.g., unique constraint violations)
        await db.rollback()  # Explicit rollback if the transaction block was exited early
        raise HTTPException(status_code=400, detail=f"Database integrity error. {str(e)}")
    except Exception as e:
        await db.rollback()  # Rollback for other exceptions
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred. {str(e)}")
    
@app.put('/api/update-item/{id}')
async def update_item(
        id: int,
        item_edit: ItemEdit,
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(get_current_user)  # Validate token
):
    try:
        # Use a transaction block
        async with db.begin():
            created_date_now = datetime.now()
            # Fetch the user to update
            result = await db.execute(select(Item).where(Item.id == id))
            item = result.scalars().first()

            if not item:
                raise HTTPException(status_code=404, detail="User not found.")

            # Update item fields
            item.name = item_edit.name.upper()
            item.description = item_edit.description
            item.updated_by = current_user.get("sub")
            item.updated_date = created_date_now

            # Log the update action
            system_log = System_logs(
                description=f"Item {item.name} updated successfully.",
                user_id=current_user.get("id"),
                created_by=current_user.get("sub"),
                created_date=created_date_now
            )
            db.add(system_log)

            # No explicit commit is needed; changes are committed if no exceptions occur

        return {"detail": "Item successfully updated."}
    except IntegrityError as e:
        # Handle integrity errors (e.g., unique constraint violations)
        await db.rollback()  # Explicit rollback if the transaction block was exited early
        raise HTTPException(status_code=400, detail=f"Database integrity error. {str(e)}")

    except Exception as e:
        # Rollback the transaction if an exception occurs
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred. {str(e)}")

@app.delete('/api/delete-item/{id}')
async def delete_item(
        id: int,
        db: AsyncSession = Depends(get_db),
        current_user: dict = Depends(get_current_user)  # Validate token
):
    try:
        async with db.begin():  # Use a transaction block
            # Fetch the item to delete
            result = await db.execute(select(Item).where(Item.id == id))
            item = result.scalars().first()

            if not item:
                raise HTTPException(status_code=404, detail="Item not found.")

            # Delete the item
            await db.delete(item)

            # Log the deletion action
            system_log = System_logs(
                description=f"Item {item.name} deleted successfully.",
                user_id=current_user.get("id"),
                created_by=current_user.get("sub"),
                created_date=datetime.now()
            )
            db.add(system_log)

        return {"detail": "Item successfully deleted."}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred. {str(e)}")