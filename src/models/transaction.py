import enum

from src.models.base_model import BaseModel

from sqlalchemy import (
    Enum,
    Column,
    String,
    Float,
    ForeignKey
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class TransactionType(enum.Enum):
    deposit='deposit'
    withdraw='withdraw'
    expense='expense'


class TransactionStatus(enum.Enum):
    acepted='acepted'
    rejected='rejected'


class Transaction(BaseModel):
    __tablename__ = 'transactions'

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    name = Column(String, nullable=False)
    merchant = Column(String)
    transaction_type = Column(
        Enum(TransactionType),
        default=TransactionType.deposit,
        nullable=False
    )
    status = Column(
        Enum(TransactionStatus),
        default=TransactionStatus.acepted,
        nullable=False
    )
    amount = Column(Float, nullable=False)

    user = relationship(
        'User',
        lazy='joined',
        back_populates='transactions',
        viewonly=True
    )
