from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from developers.models import (
    Developer,
    University,
    Education,
    Company,
    Employment,
    Skill,
)


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

    def test_developer_with_employment_history(self):
        linux_foundation = Company.objects.create(name='Linux Foundation')
        Employment.objects.create(
            developer=self.torvalds,
            company=linux_foundation,
            role='OSDL Fellow',
            from_date=datetime(year=2003, month=1, day=1),
            to_date=None
        )

        response = self.client.get('/developers/1/')

        self.assertListEqual(response.json()['employment_history'], [{
            'company': {'name': 'Linux Foundation'},
            'role': 'OSDL Fellow',
            'from': '2003-01-01',
            'to': None,
        }])

    def test_currently_unemployed_developer(self):
        achistyakov = Developer.objects.create(name='Alexander', surname='Chistyakov')
        fsecure = Company.objects.create(name='F-Secure Inc.')
        vispamedia = Company.objects.create(name='VispaMedia Inc.')
        Employment.objects.create(
            developer=achistyakov,
            company=fsecure,
            role='Test Engineer',
            from_date=datetime(year=2012, month=4, day=1),
            to_date=datetime(year=2015, month=7, day=1),
        )
        Employment.objects.create(
            developer=achistyakov,
            company=vispamedia,
            role='Test Automation Engineer',
            from_date=datetime(year=2016, month=7, day=1),
            to_date=datetime(year=2017, month=12, day=1),
        )

        response = self.client.get('/developers/2/')

        self.assertListEqual(response.json()['employment_history'], [
            {'company': {'name': 'F-Secure Inc.'},
             'role': 'Test Engineer',
             'from': '2012-04-01',
             'to': '2015-07-01'},
            {'company': {'name': 'VispaMedia Inc.'},
             'role': 'Test Automation Engineer',
             'from': '2016-07-01',
             'to': '2017-12-01'},
        ])


# TODO: replace self.assertEqual with specific self.assertDictEqual, self.assertListEqual
# for better error messages

class DevelopersListTestCase(TestCase):
    def setUp(self):
        self.wozniak = Developer.objects.create(name='Stephen', surname='Wozniak')
        self.stallman = Developer.objects.create(name='Richard', surname='Stallman')

        self.harvard_university = University.objects.create(name='Harvard University')
        self.mit_university = University.objects.create(name='Massachusetts Institute of Technology (MIT)')

        self.hp = Company.objects.create(name='Hewlett-Packard')

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

    def test_developers_list_with_employment_history(self):
        Employment.objects.create(
            developer=self.wozniak,
            company=self.hp,
            role='Intern',
            from_date=datetime(year=1975, month=1, day=1),
            to_date=datetime(year=1976, month=4, day=1),
        )

        response = self.client.get('/developers/')

        self.assertListEqual(response.json()[0]['employment_history'], [
            {'company': {'name': 'Hewlett-Packard'},
             'role': 'Intern',
             'from': '1975-01-01',
             'to': '1976-04-01', },
        ])
        self.assertListEqual(response.json()[1]['employment_history'], [])

    def test_filter_developers_by_skills(self):
        unix_skill = Skill.objects.create(title='Unix')
        lisp_skill = Skill.objects.create(title='Lisp')
        emacs_skill = Skill.objects.create(title='Emacs')
        electronic_skill = Skill.objects.create(title='Electronic')

        Developer.objects.create(name='No skills')

        self.wozniak.skills.add(electronic_skill, unix_skill)
        self.stallman.skills.add(unix_skill, lisp_skill, emacs_skill)

        response = self.client.get('/developers/?skill=Lisp')
        self.assertListEqual(
            response.json(), [
                {'name': 'Richard', 'surname': 'Stallman',
                 'skills': ['Unix', 'Lisp', 'Emacs'],
                 'educations': [], 'employment_history': []},
            ]
        )

        response = self.client.get('/developers/?skill=Unix')
        self.assertListEqual(
            response.json(), [
                {'name': 'Stephen', 'surname': 'Wozniak',
                 'skills': ['Unix', 'Electronic'],
                 'educations': [], 'employment_history': []},
                {'name': 'Richard', 'surname': 'Stallman',
                 'skills': ['Unix', 'Lisp', 'Emacs'],
                 'educations': [], 'employment_history': []},
            ]
        )

        response = self.client.get('/developers/?skill=Unix&skill=Lisp')
        self.assertListEqual(
            response.json(), [
                {'name': 'Richard', 'surname': 'Stallman',
                 'skills': ['Unix', 'Lisp', 'Emacs'],
                 'educations': [], 'employment_history': []},
            ]
        )
