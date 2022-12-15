# https://www.moesif.com/blog/technical/api-design/REST-API-Design-Filtering-Sorting-and-Pagination/

from typing import Any

from src.schemas.filters import FilterSchema


class QueryParameterParse(object):

    @classmethod
    def _cast_query_value(cls, value: str) -> Any:
        pass

    @classmethod
    def _get_query_operator(cls, field: str) -> str:
        pass

    @classmethod
    def transform_query_params(cls, query_params: dict) -> list[FilterSchema]:
        """Transform query params into a list of simple filters.

        Args:
            -   query_params: dict = Query params that represents filters
            to be applied to endpoint data.

        Returns:
            -   list[FilterSchema] = List filters from query params
            represented as FilterSchema filters for queries.
        """

        filters: list[FilterSchema] = []
        for param, value in query_params.items():
            op = cls._get_query_operator(param)
            casted_value = cls._cast_query_value(value)

            filters.append(
                FilterSchema(
                    field_name=param,
                    operation=op,
                    value=casted_value
                )
            )

        return filters
