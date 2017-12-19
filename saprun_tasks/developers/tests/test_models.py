from datetime import datetime

from django.core.exceptions import ValidationError
from django.test import TestCase

from developers.models import (
    Skill,
    Company,
    University,
    Developer,
    Education,
    Employment,
)


class SkillModelTestCase(TestCase):
    def test_string_representation(self):
        tdd_skill = Skill.objects.create(name='TDD')

        self.assertEqual(str(tdd_skill), 'TDD')


class CompanyModelTestCase(TestCase):
    def test_string_representation(self):
        google_inc = Company.objects.create(name='Alphabet')

        self.assertEqual(str(google_inc), 'Alphabet')


class UniversityModelTestCase(TestCase):
    def test_string_representation(self):
        itmo = University.objects.create(name='ITMO University')

        self.assertEqual(str(itmo), 'ITMO University')


class DeveloperModelTestCase(TestCase):
    def test_string_representation(self):
        ada = Developer.objects.create(name='Ada', surname='Lovelace')

        self.assertEqual(str(ada), 'Ada Lovelace')

    def test_string_representation_no_surname(self):
        lulz_sec = Developer.objects.create(name='LulzSec')

        self.assertEqual(str(lulz_sec), 'LulzSec')


class EducationModelTestCase(TestCase):
    def test_string_representation(self):
        khnut = Developer.objects.create(name='Donald', surname='Knuth')
        caltech = University.objects.create(name='California Institute of Technology')
        khnut_education = Education.objects.create(
            developer=khnut,
            university=caltech,
            year_of_graduation=1963,
        )

        self.assertEqual(
            str(khnut_education),
            'Donald Knuth graduated from California Institute of Technology at 1963'
        )

    def test_education_year_min_restrictions(self):
        helsinki_university = University.objects.create(name='University of Helsinki')
        torvalds = Developer.objects.create(name='Linus', surname='Torvalds')

        education = Education.objects.create(
            developer=torvalds,
            university=helsinki_university,
            year_of_graduation=1899,
        )

        self.assertRaises(ValidationError, education.full_clean)


class EmploymentModelTestCase(TestCase):
    def test_string_representation(self):
        carmack = Developer.objects.create(name='John', surname='Carmack')
        oculus = Company.objects.create(name='Oculus VR')
        id_software = Company.objects.create(name='id Software LLC')
        carmack_oculus = Employment.objects.create(
            developer=carmack,
            company=oculus,
            role='CTO',
            from_date=datetime(year=2013, month=7, day=1),
            to_date=None,
        )
        self.assertEqual(
            str(carmack_oculus),
            'John Carmack is being CTO of Oculus VR from 2013-07-01 till now'
        )

        carmack_id_software = Employment.objects.create(
            developer=carmack,
            company=id_software,
            role='co-founder',
            from_date=datetime(year=1991, month=2, day=1),
            to_date=datetime(year=2013, month=7, day=1)
        )
        self.assertEqual(
            str(carmack_id_software),
            'John Carmack was co-founder of id Software LLC from 1991-02-01 to 2013-07-01'
        )
