from django.test import TestCase
from developers.models import Developer, Skill


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

    def test_developer_with_skills(self):
        rob_pike = Developer(name='Rob', surname='Pike')
        rob_pike.save()
        rob_pike.skills.create(title='C')
        rob_pike.skills.create(title='Unix')
        rob_pike.skills.create(title='Golang')
        response = self.client.get('/developers/2/')
        self.assertEqual(response.json()['skills'], ['C', 'Unix', 'Golang'])


class DevelopersListTestCase(TestCase):
    def setUp(self):
        self.wozniak = Developer(name='Stephen', surname='Wozniak')
        self.wozniak.save()
        self.stallman = Developer(name='Richard', surname='Stallman')
        self.stallman.save()

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

    def test_developers_list_skills(self):
        self.stallman.skills.create(title='Unix')
        self.stallman.skills.create(title='Lisp')
        self.stallman.skills.create(title='Emacs')

        response = self.client.get('/developers/')

        self.assertEqual(response.json()[0]['skills'], [])
        self.assertEqual(response.json()[1]['skills'], ['Unix', 'Lisp', 'Emacs'])
