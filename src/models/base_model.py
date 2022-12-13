import uuid

from src.schemas import ORMSerializer
from src.connection.database import Base

from sqlalchemy import (
    Column,
    func,
    TIMESTAMP
)
from sqlalchemy.dialects.postgresql import UUID


class BaseModel(Base, ORMSerializer):
    __abstract__ = True

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(
        'timestamp',
        TIMESTAMP(timezone=False),
        nullable=False,
        default=func.current_timestamp()
    )
    updated_at = Column(
        'timestamp',
        TIMESTAMP(timezone=False),
        nullable=False,
        default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )
