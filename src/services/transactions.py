import uuid
from typing import Optional

from src.schemas.filters import FilterSchema
from src.models.transaction import Transaction
from src.repositories.transactions import TransactionRepository

from sqlalchemy.orm.session import Session


class TransactionService:

    def __init__(self):
        self._repo = TransactionRepository(Transaction)

    def get_user_transactions(
        self,
        user_id: uuid.UUID,
        db: Session,
        filters: Optional[list[FilterSchema]]
    ) -> list[Transaction]:
        """Fetch all transactions for specific user.
        These records are paginated and simple filters can be applied.

        Args:
            -   user_id: uuid.UUID = User id

            -   db: Session = SQLAlchemy session object.

        Returns:
            -   list[Transaction] = List of transaction of the provided user.
            This list is paginated and filtered.
        """

        if filters is None:
            filters = []

        filters.append(
            FilterSchema(
                field_name='id',
                operation='eq',
                value=user_id
            )
        )