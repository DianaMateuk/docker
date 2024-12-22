from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, Boolean, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class BaseModel(AsyncAttrs, DeclarativeBase):
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=None, nullable=True)
    deleted_at = Column(DateTime, default=None, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)
