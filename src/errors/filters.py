class InvalidFilterColumn(Exception):
    """Raises when a column does not belongs to model."""


class InvalidFilterOperator(Exception):
    """Raises when an operator is not found in Database operators."""
