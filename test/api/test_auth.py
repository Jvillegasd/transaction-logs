from test.base_case import BaseCase


class TestUserAuth(BaseCase):

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

        self.assertEqual(response.status_code, 200)
        print(response.get_json())
