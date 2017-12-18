from django.test import TestCase
from developers.models import Developer


class DevelopersListTestCase(TestCase):
    def setUp(self):
        Developer(name='Stephen', surname='Wozniak').save()
        Developer(name='Richard', surname='Stallman').save()

    def test_success_response_code(self):
        response = self.client.get('/developers/')
        self.assertEqual(response.status_code, 200)

    def test_developers_list_fields(self):
        response = self.client.get('/developers/')
        self.assertEqual(response.json(), [
            {'name': 'Stephen', 'surname': 'Wozniak',
             'skills': [], 'educations': [], 'employment_history': []},
            {'name': 'Richard', 'surname': 'Stallman',
             'skills': [], 'educations': [], 'employment_history': []},
        ])


class DeveloperTestCase(TestCase):
    def setUp(self):
        self.developer = Developer(name='Linus', surname='Torvalds')
        self.developer.save()

    def test_success_response_code(self):
        response = self.client.get('/developers/1/')
        self.assertEqual(response.status_code, 200)

    def test_developer_fields(self):
        response = self.client.get('/developers/1/')
        self.assertEqual(
            response.json(),
            {'name': 'Linus', 'surname': 'Torvalds',
             'skills': [], 'educations': [], 'employment_history': []}
        )

    def test_no_surname_developer(self):
        Developer(name='Tflow', surname=None).save()
        response = self.client.get('/developers/2/')
        self.assertEqual(
            response.json(),
            {'name': 'Tflow', 'surname': None,
             'skills': [], 'educations': [], 'employment_history': []}
        )
