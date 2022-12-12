from src.models.base_model import BaseModel

from sqlalchemy import (
    Column,
    String
)
from sqlalchemy.orm import relationship


class User(BaseModel):
    __tablename__ = 'users'

    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)

    transactions = relationship(
        'Transaction',
        back_populates='user',
        viewonly=True
    )
