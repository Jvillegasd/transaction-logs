from sqlalchemy.inspection import inspect


class ORMSerializer(object):

    def serialize(self) -> dict:
        """Transform ORM object into a dict.

        Returns:
            -   dict = Serialized ORM object.
        """
        return {
            column: getattr(self, column)
            for column in inspect(self).attrs.keys()
        }

    @staticmethod
    def serialize_list(records: list) -> list[dict]:
        """Transform ORM object list into a list of dicts.

        Returns:
            -   list[dict] = Serialized ORM object list.
        """
        return [record.serialize() for record in records]
