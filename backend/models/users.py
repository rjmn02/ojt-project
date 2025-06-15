from sqlalchemy import String, Enum, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List
import enum
import datetime
from models.base import Base  # ADDED IMPORT
from typing import TYPE_CHECKING  # UPDATED

if TYPE_CHECKING:
  from .sales_transactions import Sales_Transaction
  from .system_logs import System_Log

class AccountType(enum.Enum):
  ADMIN = "ADMIN"
  AGENT = "AGENT"
  CLIENT = "CLIENT"

class AccountStatus(enum.Enum):
  ACTIVE = "ACTIVE"
  INACTIVE = "INACTIVE"

class User(Base):
  __tablename__ = "users"

  id: Mapped[int] = mapped_column(primary_key=True, index=True)

  email: Mapped[str] = mapped_column(String(155), nullable=False, unique=True)
  password: Mapped[str] = mapped_column(String(255), nullable=False)

  firstname: Mapped[str] = mapped_column(String(155), nullable=False)
  middlename: Mapped[Optional[str]] = mapped_column(String(155), nullable=True)
  lastname: Mapped[str] = mapped_column(String(155), nullable=False)
  contact_num: Mapped[Optional[str]] = mapped_column(String(155), nullable=True)

  type: Mapped[AccountType] = mapped_column(Enum(AccountType), default=AccountType.CLIENT, nullable=False)
  status: Mapped[AccountStatus] = mapped_column(Enum(AccountStatus), default=AccountStatus.ACTIVE, nullable=False)

  created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
  updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

  # Relationships
  logs: Mapped[List["System_Log"]] = relationship(back_populates="user")
  sales_as_customer: Mapped[List["Sales_Transaction"]] = relationship(back_populates="customer", cascade="all, delete")
  sales_as_agent: Mapped[List["Sales_Transaction"]] = relationship(back_populates="agent", cascade="all, delete")