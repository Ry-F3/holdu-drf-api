from rest_framework import serializers
from .models import WorkExperience
from django.contrib.auth.models import User


class WorkExperienceSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(
        source='owner', read_only=True
    )
    owner_name = serializers.CharField(source='owner.username', read_only=True)

    class Meta:
        model = WorkExperience
        fields = ['id', 'owner_id', 'owner_name', 'job_title', 'company_name',
                  'start_date', 'end_date', 'skills', 'job_summary']

    def validate(self, data):
        """
        Check if a record with the same combination of fields already exists.
        """
        # Retrieve the field values from the validated data
        job_title = data.get('job_title')
        company_name = data.get('company_name')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        skills = data.get('skills')
        job_summary = data.get('job_summary')
        owner = data.get('owner')

        # Check if a record with the same combination of fields already exists
        if WorkExperience.objects.filter(
            job_title=job_title,
            company_name=company_name,
            start_date=start_date,
            end_date=end_date,
            skills=skills,
            job_summary=job_summary,
            owner=owner
        ).exists():
            raise serializers.ValidationError(
                "A record with the same combination of fields already exists.")

        return data
