from src.importer.importer import DataImporter
from src.connection.database import DataAccessLayer


class BaseCase:

    @classmethod
    def setup_class(cls):
        cls._import_api()
        cls.dal = DataAccessLayer()
        cls.importer = DataImporter()
        cls.importer.clear_all_models()

    @classmethod
    def teardown_class(clss):
        pass

    @classmethod
    def _import_api(cls):
        pass
