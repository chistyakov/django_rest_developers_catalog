from datetime import date

from django.test import TestCase

from developers.models import (
    Developer,
    University,
    Education,
    Company,
    Employment,
)


class AcceptanceTestCase(TestCase):
    def setUp(self):
        iivanov = Developer.objects.create(name='Иван', surname='Иванов')
        iivanov.skills.create(name='Python')
        iivanov.skills.create(name='Django')
        iivanov.skills.create(name='Django REST Framework')

        spsu = University.objects.create(name='Saint-Petersburg State University')
        Education.objects.create(
            developer=iivanov,
            university=spsu,
            year_of_graduation=2016,
        )

        hah = Company.objects.create(name='Horns and Hooves')
        Employment.objects.create(
            developer=iivanov,
            company=hah,
            role='Junior Python Developer',
            start_date=date(year=2017, month=2, day=1),
            end_date=date(year=2017, month=9, day=1)
        )

    def test_from_task_get_list(self):
        response = self.client.get('/developers/')

        self.assertListEqual(
            response.json(), [{
                # NOTE: it makes sense to add 'id' (there is /developers/<id> route)
                'name': 'Иван',
                'surname': 'Иванов',
                'skills': ['Python', 'Django', 'Django REST Framework'],
                # 'education': [{
                # RENAMED 'education' -> 'educations'
                'educations': [{
                    # 'university' -- not the best name for not higher education establishments
                    'university': {'name': 'Saint-Petersburg State University'},
                    # 'year_of_graduation': 2016,
                    # CHANGED the type from 'string' to 'int' (could be critical for non-js clients)
                    'year_of_graduation': 2016,
                }],
                'employment_history': [{
                    'company': {'name': 'Horns and Hooves'},
                    'role': 'Junior Python Developer',
                    'from': '2017-02-01', 'to': '2017-09-01'
                }],
            }]
        )

    def test_from_task_get_single_dev(self):
        response = self.client.get('/developers/1/')

        self.assertDictEqual(
            response.json(), {
                'name': 'Иван',
                'surname': 'Иванов',
                'skills': ['Python', 'Django', 'Django REST Framework'],
                'educations': [{
                    'university': {'name': 'Saint-Petersburg State University'},
                    'year_of_graduation': 2016,
                }],
                'employment_history': [{
                    'company': {'name': 'Horns and Hooves'},
                    'role': 'Junior Python Developer',
                    'from': '2017-02-01', 'to': '2017-09-01'
                }],
            }
        )
