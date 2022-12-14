from typing import Optional, Any
from dataclasses import dataclass

from src.schemas.base_schema import BaseSchema


@dataclass
class PaginationCursor(BaseSchema):
    prev: Optional[int]
    next: int
    per_page: int


@dataclass
class ModelPagination(BaseSchema):
    records: list[Any]
    cursor: PaginationCursor
