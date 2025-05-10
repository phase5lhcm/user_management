from __future__ import annotations
from sqlalchemy import String, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.database import Base
from typing import TYPE_CHECKING
from uuid import UUID
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID

    
if TYPE_CHECKING:
    from app.models.user_model import User

class Event(Base):
    __tablename__ = 'events'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    creator_id: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    creator: Mapped["User"] = relationship(back_populates="events")

    
