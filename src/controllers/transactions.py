from src.connection import get_dal
from src.middlewares.auth import is_authenticated
from src.services.transactions import TransactionService
from src.utils.filters_parser import QueryParameterParser

from flask import Blueprint, session, request

transactions_api = Blueprint('transactions', __name__)
transaction_service = TransactionService()


@transactions_api.get('/')
@is_authenticated
def user_transactions():
    with get_dal().get_session() as db:
        user_id = session.get('user_id')
        filters = QueryParameterParser.transform_query_params(
            request.args.to_dict()
        )

        transactions = transaction_service.get_user_transactions(
            user_id,
            db,
            filters
        )
        transactions_serialized = transactions.dict()

    return transactions_serialized
