from datetime import datetime

from django.test import TestCase

from developers.models import (
    Developer,
    University,
    Education,
    Company,
    Employment,
    Skill,
)


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

        self.assertListEqual(response.json(), [
            {'name': 'Stephen', 'surname': 'Wozniak',
             'skills': [], 'educations': [], 'employment_history': []},
            {'name': 'Richard', 'surname': 'Stallman',
             'skills': [], 'educations': [], 'employment_history': []},
        ])

    def test_developers_list_skills(self):
        self.stallman.skills.create(name='Unix')
        self.stallman.skills.create(name='Lisp')
        self.stallman.skills.create(name='Emacs')

        response = self.client.get('/developers/')

        self.assertListEqual(response.json()[0]['skills'], [])
        self.assertListEqual(response.json()[1]['skills'], ['Unix', 'Lisp', 'Emacs'])

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

        self.assertListEqual(response.json()[0]['educations'], [])
        self.assertListEqual(response.json()[1]['educations'], [
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
        unix_skill = Skill.objects.create(name='Unix')
        lisp_skill = Skill.objects.create(name='Lisp')
        emacs_skill = Skill.objects.create(name='Emacs')
        electronic_skill = Skill.objects.create(name='Electronic')

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
