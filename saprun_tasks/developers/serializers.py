from rest_framework import serializers

from developers.models import Developer


class DeveloperSerializer(serializers.ModelSerializer):
    skills = serializers.StringRelatedField(many=True)

    class Meta:
        model = Developer
        exclude = ('id', )
