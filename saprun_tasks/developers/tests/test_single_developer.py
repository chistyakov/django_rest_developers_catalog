from datetime import date

from django.test import TestCase

from developers.models import (
    Developer,
    University,
    Education,
    Company,
    Employment,
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

        self.assertDictEqual(
            response.json(),
            {'name': 'Linus', 'surname': 'Torvalds',
             'skills': [], 'educations': [], 'employment_history': []}
        )

    def test_no_surname_developer(self):
        Developer(name='Tflow', surname=None).save()

        response = self.client.get('/developers/2/')

        self.assertDictEqual(
            response.json(),
            {'name': 'Tflow', 'surname': None,
             'skills': [], 'educations': [], 'employment_history': []}
        )

    def test_developer_with_skills(self):
        rob_pike = Developer.objects.create(name='Rob', surname='Pike')
        rob_pike.skills.create(name='C')
        rob_pike.skills.create(name='Unix')
        rob_pike.skills.create(name='Golang')

        response = self.client.get('/developers/2/')

        self.assertListEqual(response.json()['skills'], ['C', 'Unix', 'Golang'])

    def test_developer_with_education(self):
        Education.objects.create(
            developer=self.torvalds,
            university=self.helsinki_university,
            year_of_graduation=1996,
        )

        response = self.client.get('/developers/1/')

        self.assertListEqual(
            response.json()['educations'],
            [{'university': {'name': 'University of Helsinki'},
              'year_of_graduation': 1996}]
        )

    def test_developer_with_employment_history(self):
        linux_foundation = Company.objects.create(name='Linux Foundation')
        Employment.objects.create(
            developer=self.torvalds,
            company=linux_foundation,
            role='OSDL Fellow',
            from_date=date(year=2003, month=1, day=1),
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
            from_date=date(year=2012, month=4, day=1),
            to_date=date(year=2015, month=7, day=1),
        )
        Employment.objects.create(
            developer=achistyakov,
            company=vispamedia,
            role='Test Automation Engineer',
            from_date=date(year=2016, month=7, day=1),
            to_date=date(year=2017, month=12, day=1),
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
