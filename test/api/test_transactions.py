from test.base_case import BaseCase


class TestApiTransaction(BaseCase):

    def setUp(self):
        self.users = self.importer.load_model('users')
        self.transactions = self.importer.load_model('transactions')

    def tearDown(self):
        self.importer.clear_model('transactions')
        self.importer.clear_model('users')

    def test_get_user_transactions(self):
        data = self.users[0]
        with self.client.session_transaction() as session:
            session['user_id'] = data['id']
        
        response = self.client.get('/api/transactions/')
        response_json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response_json['records']), 0)
        print(response_json)
