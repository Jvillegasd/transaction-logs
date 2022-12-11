from test.base_case import BaseCase
from src.models.user import User
from src.models.transaction import Transaction



class TestImporterSeeds(BaseCase):

    def setup_class(self):
        super().setup_class()

    def setup_method(self):
        self.importer.clear_all_models()

    def test_load_all_models(self):
        self.importer.load_all_models()

        with self.dal.get_session() as db:
            user_record = db.query(User).first()
            transaction_record = db.query(Transaction).first()

        assert user_record is not None
        assert transaction_record is not None

    def test_clear_all_models(self):
        self.importer.clear_all_models()

        with self.dal.get_session() as db:
            user_record = db.query(User).first()
            transaction_record = db.query(Transaction).first()

        assert user_record is None
        assert transaction_record is None
