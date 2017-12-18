from django.test import TestCase


class DevelopersListTestCase(TestCase):
    def test_success_response_code(self):
        response = self.client.get('/developers/')
        self.assertEqual(response.status_code, 200)
