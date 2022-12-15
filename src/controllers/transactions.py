from src.connection import get_dal
from src.middlewares.auth import is_authenticated
from src.services.transactions import TransactionService
from src.utils.filters_parser import QueryParameterParser
from src.schemas.model_pagination import QueryParamPagination

from flask import Blueprint, session, request

transactions_api = Blueprint('transactions', __name__)
transaction_service = TransactionService()


@transactions_api.get('/')
@is_authenticated
def user_transactions():
    with get_dal().get_session() as db:
        user_id = session.get('user_id')
        query_params: dict = request.args.to_dict()

        paginate = QueryParamPagination(
            next_cursor=query_params.pop('next_cursor', None),
            per_page=query_params.pop('per_page', None)
        )
        filters = QueryParameterParser.transform_query_params(
            query_params
        )

        transactions = transaction_service.get_user_transactions(
            user_id=user_id,
            db=db,
            filters=filters,
            pagination=paginate
        )
        transactions_serialized = transactions.dict()

    return transactions_serialized
