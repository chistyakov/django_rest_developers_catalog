from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=300, unique=True)

    def __str__(self):
        return self.name


class Company(models.Model):
    name = models.CharField(max_length=400, unique=True)

    def __str__(self):
        return self.name


class University(models.Model):
    name = models.CharField(max_length=400, unique=True)

    def __str__(self):
        return self.name


class Developer(models.Model):
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120, blank=True, null=True)
    skills = models.ManyToManyField(Skill, related_name='developers', blank=True)
    educations = models.ManyToManyField(
        University, through='Education',
        related_name='graduated', blank=True
    )
    employment_history = models.ManyToManyField(
        Company, through='Employment',
        related_name='employees_history', blank=True
    )

    def __str__(self):
        if not self.surname:
            return self.name
        return f'{self.name} {self.surname}'


class Education(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    year_of_graduation = models.IntegerField(
        validators=(MinValueValidator(1900),)
        # don't add MaxValueValidator(currentyear) to allow ungraduated developers
    )

    def __str__(self):
        return (f'{self.developer} graduated '
                f'from {self.university} at {self.year_of_graduation}')


# The MaxValueValidator executed only once:
# https://stackoverflow.com/a/41422670
def less_then_now_validator(value):
    if value and value > datetime.now().date():
        raise ValidationError('date should be less then now')


class Employment(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    role = models.CharField(max_length=200)
    from_date = models.DateField(
        validators=(less_then_now_validator, )
    )
    to_date = models.DateField(
        null=True,
        validators=(less_then_now_validator,)
    )

    def __str__(self):
        if self.to_date:
            return (f'{self.developer} was {self.role} of {self.company} '
                    f'from {self.from_date:%Y-%m-%d} to {self.to_date:%Y-%m-%d}')
        else:
            return (f'{self.developer} is being {self.role} of {self.company} '
                    f'from {self.from_date:%Y-%m-%d} till now')

    def clean(self):
        if self.to_date and self.to_date < self.from_date:
            raise ValidationError('start of employment should be greater then end')
