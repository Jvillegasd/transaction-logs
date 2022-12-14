from src.models.base_model import BaseModel
from src.models.transaction import Transaction, TransactionStatus

from sqlalchemy import (
    Column,
    String,
    func,
    select
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property


class User(BaseModel):
    __tablename__ = 'users'

    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    transactions = relationship(
        'Transaction',
        backref='user'
    )

    @hybrid_property
    def account_balance(self) -> float:
        return float(sum(
            transaction.amount
            for transaction in self.transactions
            if transaction.status == TransactionStatus.acepted
        ))

    @account_balance.expression
    def account_balance(cls):
        return (
            select([func.sum(Transaction.amount)]).
            where(
                Transaction.user_id == cls.id,
                Transaction.status == TransactionStatus.acepted
            ).label('account_balance')
        )

    def serialize(self) -> dict:
        serialized = super().serialize()
        serialized.pop('password', None)
        return serialized
