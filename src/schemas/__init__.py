import datetime

from sqlalchemy.orm import Query
from sqlalchemy.inspection import inspect


class ORMSerializer(object):

    def serialize(self) -> dict:
        """Transform ORM object into a dict.

        Returns:
            -   dict = Serialized ORM object.
        """

        serialized_obj: dict = {}
        for column in inspect(self).attrs.keys():
            value = getattr(self, column)
            if isinstance(value, Query):
                value = self.serialize_list(value.all())

            if isinstance(value, datetime.datetime):
                value = value.strftime('%d-%m-%Y %H:%M:%S')

            serialized_obj[column] = value

        return serialized_obj

    @staticmethod
    def serialize_list(records: list) -> list[dict]:
        """Transform ORM object list into a list of dicts.

        Returns:
            -   list[dict] = Serialized ORM object list.
        """
        return [record.serialize() for record in records]
