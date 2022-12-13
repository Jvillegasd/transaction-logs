from test.base_case import BaseCase


class TestApiUserAuth(BaseCase):

    def setUp(self):
        self.users = self.importer.load_model('users')

    def tearDown(self):
        self.importer.clear_model('users')

    def test_auth_endpoint(self):
        data = self.users[0]
        response = self.client.post(
            '/api/users/auth',
            headers=self.headers,
            json=data
        )
        response_json = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json['name'], data['name'])
        self.assertEqual(response_json['email'], data['email'])

    def test_auth_user_not_found(self):
        data = {
            'email': 'wrong@email.com',
            'password': 123123
        }
        response = self.client.post(
            '/api/users/auth',
            headers=self.headers,
            json=data
        )
        response_json = response.get_json()
        expected_value: dict = {
            'code': 404,
            'name': 'Not Found',
            'description': 'User not found in database'
        }

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response_json, expected_value)

    def test_auth_user_bad_creds(self):
        data = self.users[0]
        data['password'] = 'something else'

        response = self.client.post(
            '/api/users/auth',
            headers=self.headers,
            json=data
        )
        response_json = response.get_json()
        expected_value: dict = {
            'code': 401,
            'name': 'Unauthorized',
            'description': 'Password is wrong'
        }

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response_json, expected_value)
