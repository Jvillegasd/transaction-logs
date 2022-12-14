from test.base_case import BaseCase


class TestApiUsers(BaseCase):

    def setUp(self):
        self.users = self.importer.load_model('users')
        self.transactions = self.importer.load_model('transactions')

    def tearDown(self):
        self.importer.clear_model('transactions')
        self.importer.clear_model('users')

    def test_get_user_balance(self):
        data = self.users[0]
        with self.client.session_transaction() as session:
            session['user_id'] = data['id']

        response = self.client.get('/api/users/account-balance')
        response_json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('account_balance', response_json)
        self.assertEqual(type(response_json['account_balance']), float)
        self.assertGreaterEqual(response_json['account_balance'], 0)
