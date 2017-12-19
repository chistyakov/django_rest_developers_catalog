from django.core.exceptions import ValidationError
from django.test import TestCase
from developers.models import Developer, University, Education


class DeveloperTestCase(TestCase):
    def setUp(self):
        self.helsinki_university = University.objects.create(name='University of Helsinki')
        self.torvalds = Developer.objects.create(name='Linus', surname='Torvalds')

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
        rob_pike = Developer.objects.create(name='Rob', surname='Pike')
        rob_pike.skills.create(title='C')
        rob_pike.skills.create(title='Unix')
        rob_pike.skills.create(title='Golang')
        response = self.client.get('/developers/2/')
        self.assertEqual(response.json()['skills'], ['C', 'Unix', 'Golang'])

    def test_developer_with_education(self):
        Education.objects.create(
            developer=self.torvalds,
            university=self.helsinki_university,
            year_of_graduation=1996,
        )

        response = self.client.get('/developers/1/')
        self.assertEqual(
            response.json()['educations'],
            [{'university': {'name': 'University of Helsinki'},
              'year_of_graduation': 1996}]
        )

    def test_education_year_min_restrictions(self):
        education = Education.objects.create(
            developer=self.torvalds,
            university=self.helsinki_university,
            year_of_graduation=1899,
        )
        self.assertRaises(ValidationError, education.full_clean)


class DevelopersListTestCase(TestCase):
    def setUp(self):
        self.wozniak = Developer.objects.create(name='Stephen', surname='Wozniak')
        self.stallman = Developer.objects.create(name='Richard', surname='Stallman')

        self.harvard_university = University.objects.create(name='Harvard University')
        self.mit_university = University.objects.create(name='Massachusetts Institute of Technology (MIT)')

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

    def test_developers_list_with_educations(self):
        Education.objects.create(
            developer=self.stallman,
            university=self.harvard_university,
            year_of_graduation=1974,
        )
        Education.objects.create(
            developer=self.stallman,
            university=self.mit_university,
            year_of_graduation=1975,
        )

        response = self.client.get('/developers/')

        self.assertEqual(response.json()[0]['educations'], [])
        self.assertEqual(response.json()[1]['educations'], [
            {'university': {'name': 'Harvard University'},
             'year_of_graduation': 1974},
            {'university': {'name': 'Massachusetts Institute of Technology (MIT)'},
             'year_of_graduation': 1975},
        ])
