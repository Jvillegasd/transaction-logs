from test.base_case import BaseCase
from src.models.user import User
from src.models.transaction import Transaction

from sqlalchemy.orm import Session



class TestImporterSeeds(BaseCase):

    def setUp(self):
        self.importer.clear_all_models()

    def test_load_all_models(self):
        self.importer.load_all_models()

        with self.dal.get_session() as db:
            user_record = db.query(User).first()
            transaction_record = db.query(Transaction).first()

            self.assertIsNotNone(user_record)
            self.assertIsNotNone(transaction_record)

    def test_clear_all_models(self):
        self.importer.clear_all_models()

        with self.dal.get_session() as db:
            user_record = db.query(User).first()
            transaction_record = db.query(Transaction).first()

            self.assertIsNone(user_record)
            self.assertIsNone(transaction_record)
