from typing import Optional
from dataclasses import dataclass

from src.models.base_model import BaseModel
from src.schemas.base_schema import BaseSchema


@dataclass
class PaginationCursor(BaseSchema):
    prev: Optional[int]
    next: int
    per_page: int


@dataclass
class ModelPagination(BaseSchema):
    records: list[BaseModel]
    cursor: PaginationCursor
