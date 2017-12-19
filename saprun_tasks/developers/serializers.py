from rest_framework import serializers

from developers.models import Developer, Education, University, Company, Employment


class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = ('name',)


class EducationSerializer(serializers.ModelSerializer):
    university = UniversitySerializer()

    class Meta:
        model = Education
        fields = ('university', 'year_of_graduation')


class CompanySerializers(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name',)


class EmploymentSerializer(serializers.ModelSerializer):
    company = CompanySerializers()
    start_date = serializers.DateField(source='start_date')
    to = serializers.DateField(source='end_date')

    class Meta:
        model = Employment
        fields = ('company', 'role', 'from', 'to')

EmploymentSerializer._declared_fields['from'] = EmploymentSerializer._declared_fields['start_date']
del EmploymentSerializer._declared_fields['start_date']


class DeveloperSerializer(serializers.ModelSerializer):
    skills = serializers.StringRelatedField(many=True)
    educations = EducationSerializer(source='education_set', many=True)
    employment_history = EmploymentSerializer(source='employment_set', many=True)

    class Meta:
        model = Developer
        exclude = ('id',)
