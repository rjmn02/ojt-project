from sqlalchemy import String, Text, func, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
import datetime
from models.base import Base  # ADDED IMPORT
from typing import TYPE_CHECKING  # UPDATED
if TYPE_CHECKING:
    from .users import User
    from .cars import Car

class Sales_Transaction(Base):
    __tablename__ = "sales_transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(Integer, ForeignKey("cars.id"), unique=True)  # remove unique if multiple sales allowed
    customer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id")) 
    agent_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    created_by: Mapped[str] = mapped_column(String(155))
    updated_by: Mapped[str] = mapped_column(String(155))

    car: Mapped["Car"] = relationship(
      back_populates="sale_transaction",
      foreign_keys=[car_id]
    )
    customer: Mapped["User"] = relationship(
      back_populates="sales_as_customer",
      foreign_keys=[customer_id]
    )
    agent: Mapped["User"] = relationship(
      back_populates="sales_as_agent",
      foreign_keys=[agent_id]
    )