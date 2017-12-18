from rest_framework import viewsets

from developers.models import Developer
from developers.serializers import DeveloperSerializer


class DeveloperViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DeveloperSerializer
    queryset = Developer.objects.all()
