from __future__ import annotations
from sqlalchemy import String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from typing import TYPE_CHECKING

    
if TYPE_CHECKING:
    from app.models.user_model import User

class Event(Base):
    __tablename__ = 'events'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    creator: Mapped["User"] = relationship(back_populates="events")

    
