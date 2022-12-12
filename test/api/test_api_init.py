from test.base_case import BaseCase


class TestApiLaunch(BaseCase):

    def test_home_endpoint(self):
        response = self.client.get('/api/')
        expected_value: dict = {'message': '🚀 Server is up!'}

        self.assertEqual(
            expected_value,
            response.get_json()
        )
