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
