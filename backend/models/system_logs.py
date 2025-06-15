
from sqlalchemy import Integer, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
import datetime
from models.base import Base  # ADDED IMPORT
from typing import TYPE_CHECKING  # UPDATED
if TYPE_CHECKING:
    from .users import User
    
class System_Log(Base):
    __tablename__ = "system_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    action: Mapped[Optional[str]] = mapped_column(Text)
    timestamp: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    user: Mapped["User"] = relationship(back_populates="logs")