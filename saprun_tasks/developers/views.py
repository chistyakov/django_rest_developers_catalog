from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from developers.filters import SkillFilter
from developers.models import Developer
from developers.serializers import DeveloperSerializer


class DeveloperViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DeveloperSerializer
    queryset = Developer.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filter_class = SkillFilter
