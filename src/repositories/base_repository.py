from typing import Optional, Any

from src.models.base_model import BaseModel
from src.schemas.filters import FilterSchema
from src.schemas.model_pagination import (
    ModelPagination,
    PaginationCursor,
    QueryParamPagination
)
from src.errors.filters import InvalidFilterColumn, InvalidFilterOperator

from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session


class BaseRepository:

    def __init__(self, model: BaseModel):
        self.model = model

    def find_one(
        self,
        db: Session,
        filters: list[FilterSchema]
    ) -> Optional[BaseModel]:
        """Find one record from current model that
        match simple filters.

        Args:
            -   db: Session = SQLAlchemy session.

            -   filters: list[FilterSchema] = List of simple
            filters for apply to current model.

        Returns:
            -   BaseModel = Record that match provided filters.
        """

        query = db.query(self.model)
        query = self._apply_filters(query, filters)
        return query.first()

    def find_all(
        self,
        db: Session,
        filters: list[FilterSchema]
    ) -> Query:
        """Find all records from current model that
        match simple filters.

        Args:
            -   db: Session = SQLAlchemy session.

            -   filters: list[FilterSchema] = List of simple
            filters for apply to current model.

        Returns:
            -   Query = Query of current models that match
            provided filters. Query is returned due to allows pagination
            application.
        """

        query = db.query(self.model)
        query = self._apply_filters(query, filters)
        return query

    def find_by_id(self, db: Session, id: Any) -> Optional[BaseModel]:
        """Find a record for loaded model by searching
        by id.

        Args:
            -   db: Session = SQLAlchemy session.

            -   id: Any = Id to search in table.

        Returns:
            -   Optional[BaseModel] = Record if found.
        """

        query = db.query(self.model).filter(
            self.model.id == id
        ).first()
        return query

    def apply_pagination(
        self,
        query: Query,
        paginate: Optional[QueryParamPagination] = None
    ) -> ModelPagination:
        """Paginates Query using cursor technique. So,
        pagination will scales at the same time the transactions
        does. After query is paginated, result is returned in
        DESC order.

        Args:
            -   query: Query = Query to paginate.

            -   paginate: QueryParamPagination = Object that contains
            Datetime as timestamp as a cursor for pagination and how many
            records is going to be returned per page.

        Returns:
            -   ModelPagination = Pagination dict object that save cursors and
            records for current page.
        """
        import datetime

        per_page: int = 10
        cursor_timestamp: Optional[float] = None
        if paginate:
            per_page = paginate.per_page or 10
            cursor_timestamp = paginate.next_cursor

        result: list[BaseModel]
        if cursor_timestamp:
            cursor_timestamp = float(cursor_timestamp)
            cursor_date = datetime.datetime.fromtimestamp(
                cursor_timestamp
            )
            result = query.filter(
                self.model.created_at < cursor_date
            ).order_by(self.model.created_at.desc()).limit(per_page).all()
        else:
            result = query.order_by(
                self.model.created_at.desc()
            ).limit(per_page).all()

        next_cursor: Optional[int] = None
        if result:
            next_cursor = result[-1].created_at.timestamp()

        return ModelPagination(
            records=BaseModel.serialize_list(result),
            cursor=PaginationCursor(
                prev=cursor_timestamp,
                next=next_cursor,
                per_page=per_page
            )
        )

    def _apply_filters(
        self,
        query: Query,
        filters: list[FilterSchema]
    ) -> Query:
        """Apply a list of simple filters to the provided
        query. Simple filters are intented to interact with
        fields of current model. Complex operations like Joins
        or filtering by relationship fields are not allowed.

        This function only takes into account filters declared in
        ColumnOperators class from SQLAlchemy.

        Args:
            -   query: Query = Query to be filtered.

            -   filters: list[FilterSchema] = List of simple
            filters for apply to current query.

        Returns:
            -   Query = Provided query with filter applied.
        """

        for raw_filter in filters:
            column = getattr(self.model, raw_filter.field_name, None)
            if column is None:
                raise InvalidFilterColumn(
                    f'Invalid filter column {raw_filter.field_name}'
                )

            if raw_filter.operation != 'in':
                try:
                    # Get the SQLAlchemy ColumnOperators function
                    column_op = next(filter(
                        lambda e: hasattr(column, e % raw_filter.operation),
                        ['%s', '%s_', '__%s__']
                    )) % raw_filter.operation
                except StopIteration:
                    raise InvalidFilterOperator(
                        f'Invalid filter operator: {raw_filter.operation}'
                    )
                crafted_filter = getattr(column, column_op)(raw_filter.value)
            else:
                crafted_filter = column.in_(raw_filter.value)

            query = query.filter(crafted_filter)

        return query
