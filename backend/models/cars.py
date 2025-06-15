from sqlalchemy import String, Enum, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base  # ADDED IMPORT
from typing import TYPE_CHECKING  # UPDATED
import datetime
import enum
if TYPE_CHECKING:
    from .sales_transactions import Sales_Transaction

class TransmissionType(enum.Enum):
    MANUAL = "MANUAL"
    AUTOMATIC = "AUTOMATIC"

class FuelType(enum.Enum):
    PETROL = "PETROL"
    DIESEL = "DIESEL"
    ELECTRIC = "ELECTRIC"
    HYBRID = "HYBRID"

class CarStatus(enum.Enum):
    AVAILABLE = "AVAILABLE"
    SOLD = "SOLD"
    RESERVED = "RESERVED"

class Car(Base):
    __tablename__ = 'cars'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # Car details
    vin: Mapped[str] = mapped_column(String(155), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    make: Mapped[str] = mapped_column(String(155), nullable=False)
    model: Mapped[str] =  mapped_column(String(155), nullable=False)
    color: Mapped[str] = mapped_column(String(155), nullable=False)
    mileage: Mapped[int] = mapped_column(Integer, nullable=False)

    price: Mapped[int] = mapped_column(Integer, nullable=False)

    transmission_type: Mapped[TransmissionType] = mapped_column(Enum(TransmissionType), nullable=False)
    fuel_type: Mapped[FuelType] = mapped_column(Enum(FuelType), nullable=False)
    status: Mapped[CarStatus] = mapped_column(Enum(CarStatus), default=CarStatus.AVAILABLE, nullable=False)

    # Logging fields
    created_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
    created_by: Mapped[str] = mapped_column(String(155))
    updated_by: Mapped[str] = mapped_column(String(155))

    sale_transaction: Mapped["Sales_Transaction"] = relationship(back_populates="car", cascade="all, delete") 
