from typing import Any
from dataclasses import dataclass, asdict


@dataclass
class FilterSchema:
    field_name: str
    operation: str
    value: Any

    def dict(self) -> dict:
        return {k: v for k, v in asdict(self).items()}
