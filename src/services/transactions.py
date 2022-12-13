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
        filters: Optional[list[FilterSchema]] = None
    ) -> dict:
        """Fetch all transactions for specific user.
        These records are paginated and simple filters can be applied.

        Args:
            -   user_id: uuid.UUID = User id

            -   db: Session = SQLAlchemy session object.

        Returns:
            -   dict = List of transaction of the provided user.
            This list is paginated and filtered.
        """

        if filters is None:
            filters = []

        filters.append(
            FilterSchema(
                field_name='user_id',
                operation='eq',
                value=user_id
            )
        )

        transactions_query = self._repo.find_all(db, filters)
        return self._repo.apply_pagination(
            query=transactions_query
        )
