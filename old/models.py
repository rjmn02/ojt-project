from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship

from database import Base
import enum

class AccountType(enum.Enum):
    SUPER_ADMIN = "SUPER_ADMIN"
class AccountStatus(enum.Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String(255))
    middlename = Column(String(255))
    lastname = Column(String(255))
    email = Column(String(255), unique=True, nullable=False)
    contact_num = Column(String(255))
    password = Column(String(255), nullable=False)
    account_type = Column(Enum(AccountType), default=AccountType.SUPER_ADMIN, nullable=False)
    status = Column(Enum(AccountStatus), default=AccountStatus.ACTIVE, nullable=False)
    created_date = Column(DateTime(), default=datetime.now())
    created_by = Column(String(255))
    updated_date = Column(DateTime(), default=datetime.now(), onupdate=datetime.now())
    updated_by = Column(String(255))
    logs = relationship("System_logs", back_populates="user")

class System_logs(Base):
    __tablename__ = "system_logs"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(Text)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_by = Column(String(255))
    created_date = Column(DateTime(), default=datetime.now())

    user = relationship("User", back_populates="logs")

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    created_by = Column(String(255))
    updated_by = Column(String(255))
    created_date = Column(DateTime(), default=datetime.now())
    updated_date = Column(DateTime(), default=datetime.now(), onupdate=datetime.now())