import uuid

from src.connection.database import Base

from sqlalchemy import (
    Column,
    DateTime,
    func
)
from sqlalchemy.dialects.postgresql import UUID


class BaseModel(Base):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=func.current_timestamp())
    updated_at = Column(
        DateTime,
        default=func.current_timestamp,
        onupdate=func.current_timestamp
    )
