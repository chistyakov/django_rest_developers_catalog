from rest_framework import serializers

from developers.models import Developer, Education, University


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ('name',)


class EducationSerializer(serializers.ModelSerializer):
    university = UniversitySerializer()

    class Meta:
        model = Education
        fields = ('university', 'year_of_graduation')


class DeveloperSerializer(serializers.ModelSerializer):
    skills = serializers.StringRelatedField(many=True)
    educations = EducationSerializer(source='education_set', many=True)

    class Meta:
        model = Developer
        exclude = ('id',)
