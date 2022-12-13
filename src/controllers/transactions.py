from src.connection import get_dal
from src.schemas import ORMSerializer
from src.middlewares.auth import is_authenticated
from src.services.transactions import TransactionService

from flask import Blueprint, session

transactions_api = Blueprint('transactions', __name__)
transaction_service = TransactionService()


@transactions_api.get('/')
@is_authenticated
def user_transactions():
    with get_dal().get_session() as db:
        user_id = session.get('user_id')
        transactions = transaction_service.get_user_transactions(
            user_id,
            db
        )
        transactions_serialized = transactions.dict()

    return transactions_serialized
