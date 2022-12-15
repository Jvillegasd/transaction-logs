from test.base_case import BaseCase


class TestApiTransactionFilters(BaseCase):

    def setUp(self):
        self.users = self.importer.load_model('users')
        self.transactions = self.importer.load_model('transactions')

    def tearDown(self):
        self.importer.clear_model('transactions')
        self.importer.clear_model('users')

    def test_filter_by_type(self):
        data = self.users[0]
        with self.client.session_transaction() as session:
            session['user_id'] = data['id']

        response = self.client.get(
            '/api/transactions/',
            query_string={'transaction_type': 'withdraw'}
        )
        response_json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response_json['records']), 0)
        self.assertTrue(
            all(
                item['transaction_type'] == 'withdraw'
                for item in response_json['records']
            )
        )

    def test_filter_by_merchant(self):
        data = self.users[0]
        with self.client.session_transaction() as session:
            session['user_id'] = data['id']

        response = self.client.get(
            '/api/transactions/',
            query_string={'merchant': 'Starbucks'}
        )
        response_json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response_json['records']), 0)
        self.assertTrue(
            all(
                item['merchant'] == 'Starbucks'
                for item in response_json['records']
            )
        )

    def test_filter_by_merchant_and_expense(self):
        data = self.users[0]
        with self.client.session_transaction() as session:
            session['user_id'] = data['id']

        response = self.client.get(
            '/api/transactions/',
            query_string={
                'merchant': 'Starbucks',
                'transaction_type': 'expense'
            }
        )
        response_json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response_json['records']), 0)
        self.assertTrue(
            all(
                item['merchant'] == 'Starbucks' and
                item['transaction_type'] == 'expense'
                for item in response_json['records']
            )
        )

    def test_filter_by_date_range(self):
        import datetime

        data = self.users[0]
        date_format: str = '%m-%d-%Y'

        start_date = datetime.datetime.now().strftime(date_format)
        end_date = datetime.datetime.now() + datetime.timedelta(days=1)
        end_date = end_date.strftime(date_format)

        with self.client.session_transaction() as session:
            session['user_id'] = data['id']

        response = self.client.get(
            '/api/transactions/',
            query_string={
                'merchant': 'Starbucks',
                'transaction_type': 'expense',
                'created_at[ge]': start_date,
                'created_at[le]': end_date
            }
        )
        response_json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response_json['records']), 0)
        self.assertTrue(
            all(
                item['merchant'] == 'Starbucks' and
                item['transaction_type'] == 'expense'
                for item in response_json['records']
            )
        )
