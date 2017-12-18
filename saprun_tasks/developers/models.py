from django.db import models


class Skill(models.Model):
    title = models.CharField(max_length=240)

    def __str__(self):
        return self.title


class Education(models.Model):
    pass


class Company(models.Model):
    pass


class Developer(models.Model):
    name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120, blank=True, null=True)
    skills = models.ManyToManyField(Skill, related_name='developers', blank=True)
    educations = models.ManyToManyField(Education, related_name='developers', blank=True)
    employment_history = models.ManyToManyField(
        Company, related_name='developers_history', blank=True
    )
