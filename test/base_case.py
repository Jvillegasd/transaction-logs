import uuid
import unittest
from typing import Optional, Iterator

from src import create_app
from src.importer.importer import DataImporter
from src.connection.database import DataAccessLayer


class BaseCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls._import_api()
        cls.dal = DataAccessLayer()
        cls.dal.create_tables()

        cls.importer = DataImporter()
        cls.importer.clear_all_models()

    @classmethod
    def tearDownClass(cls):
        pass

    @classmethod
    def _import_api(cls):
        cls.app = create_app(config_name='test')
        cls.client = cls.app.test_client()
        cls.headers = {
            'Content-Type': 'application/json'
        }

    def authentication(
        self,
        user_id: Optional[uuid.UUID]
    ) -> Iterator:
        with self.client.session_transaction() as session:
            session['user_id'] = user_id
            yield session
