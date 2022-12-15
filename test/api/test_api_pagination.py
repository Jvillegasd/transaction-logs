from test.base_case import BaseCase


class TestApiTransactionPagination(BaseCase):

    def setUp(self):
        self.users = self.importer.load_model('users')
        self.transactions = self.importer.load_model('transactions')

    def tearDown(self):
        self.importer.clear_model('transactions')
        self.importer.clear_model('users')

    def test_get_user_transactions_per_page(self):
        data = self.users[0]
        with self.client.session_transaction() as session:
            session['user_id'] = data['id']
        
        response = self.client.get(
            '/api/transactions/',
            query_string={'per_page': 2}
        )
        response_json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response_json['records']), 2)
        self.assertIn('cursor', response_json)

    def test_get_user_transactions_all_pagination(self):
        data = self.users[0]
        with self.client.session_transaction() as session:
            session['user_id'] = data['id']
        
        response = self.client.get(
            '/api/transactions/',
            query_string={'per_page': 2}
        )
        response_json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response_json['records']), 2)
        self.assertIn('cursor', response_json)

        response_next_page = self.client.get(
            '/api/transactions/',
            query_string={
                'per_page': 2,
                'next_cursor': response_json['cursor']['next']
            }
        )
        next_page_json = response_next_page.get_json()

        self.assertEqual(response_next_page.status_code, 200)
        self.assertLessEqual(len(next_page_json['records']), 2)
        self.assertEqual(
            next_page_json['cursor']['prev'],
            response_json['cursor']['next']
        )

    def test_get_user_transactions_next_cursor(self):
        data = self.users[0]
        with self.client.session_transaction() as session:
            session['user_id'] = data['id']
        
        response = self.client.get('/api/transactions/')
        response_json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(response_json['records']), 10)
        self.assertIn('cursor', response_json)

        response_next_page = self.client.get(
            '/api/transactions/',
            query_string={
                'next_cursor': response_json['cursor']['next']
            }
        )
        next_page_json = response_next_page.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertLessEqual(len(next_page_json['records']), 3)
        self.assertEqual(
            next_page_json['cursor']['prev'],
            response_json['cursor']['next']
        )
