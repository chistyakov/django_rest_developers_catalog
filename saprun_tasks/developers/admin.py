from django.contrib import admin

from developers.models import (
    Developer,
    Skill,
    Education,
    Company,
    University,
    Employment,
)

admin.site.register(Developer)
admin.site.register(Skill)
admin.site.register(Education)
admin.site.register(Company)
admin.site.register(University)
admin.site.register(Employment)
