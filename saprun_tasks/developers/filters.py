from django.forms.fields import MultipleChoiceField
from django_filters import rest_framework as filters
from django_filters.filters import MultipleChoiceFilter

from developers.models import Developer


# https://github.com/carltongibson/django-filter/issues/137#issuecomment-37820702
class MultipleField(MultipleChoiceField):
    def valid_value(self, value):
        return True


class MultipleFilter(MultipleChoiceFilter):
    field_class = MultipleField


class SkillFilter(filters.FilterSet):
    skill = MultipleFilter(field_name='skills__name', lookup_expr='in', conjoined=True)

    class Meta(object):
        model = Developer
        fields = ('skill',)
