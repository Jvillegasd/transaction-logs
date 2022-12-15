from test.base_case import BaseCase


class TestApiTransactionFilters(BaseCase):

    def setUp(self):
        self.users = self.importer.load_model('users')
        self.transactions = self.importer.load_model('transactions')

    def tearDown(self):
        self.importer.clear_model('transactions')
        self.importer.clear_model('users')

    