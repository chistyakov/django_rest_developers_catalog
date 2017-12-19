from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from datetime import datetime


class Skill(models.Model):
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class Company(models.Model):
    pass


class University(models.Model):
    name = models.CharField(max_length=400)


class Developer(models.Model):
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120, blank=True, null=True)
    skills = models.ManyToManyField(Skill, related_name='developers', blank=True)
    educations = models.ManyToManyField(
        University, through='Education',
        related_name='graduated', blank=True
    )
    employment_history = models.ManyToManyField(
        Company, related_name='employers_history', blank=True
    )


class Education(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    year_of_graduation = models.IntegerField(
        validators=(MinValueValidator(1900), )
        # don't add MaxValueValidator(currentyear) to allow ungraduated developers
    )
