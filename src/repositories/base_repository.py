import datetime
from typing import Optional, Any

from src.models.base_model import BaseModel

from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session


class BaseRepository:

    def __init__(self, model: BaseModel):
        self.model = model

    def find_by_id(self, db: Session, id: Any) -> Optional[BaseModel]:
        """Find a record for loaded model by searching
        by id.

        Args:
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
        cursor_timestamp: Optional[float],
        per_page: int = 10
    ) -> dict:
        """Paginates Query using cursor technique. So,
        pagination will scales at the same time the transactions
        does.

        Args:
            -   query: Query = Query to paginate.

            -   cursor_timestamp: float = Datetime as timestamp as
            a cursor for pagination.

            -   per_page: int = How many records is going to be returned
            per page.

        Returns:
            -   dict = Pagination dict object that save cursors and
            records for current page.
        """

        result: list[BaseModel] = query.filter(
            self.model.created_at < cursor_timestamp
        ).order_by(self.model.created_at.asc()).limit(per_page).all()

        return {
            'records': result,
            'cursor': {
                'prev': cursor_timestamp,
                'next': result[-1].created_at,
                'per_page': per_page
            }
        }

    def apply_filters(self):
        pass
