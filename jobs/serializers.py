from rest_framework import serializers
from .models import Job, Application
from profiles.models import Profile
from django.contrib.auth.models import User
from profiles.serializers import (
    BaseProfileSerializer, EmployeeProfileSerializer,
    EmployerProfileSerializer
)


class JobSerializer(serializers.ModelSerializer):
    employer_profile = EmployerProfileSerializer(read_only=True)
    applicants = BaseProfileSerializer(many=True, read_only=True)
    is_applied = serializers.SerializerMethodField(default=False)
    job_listing_id = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ['employer_profile', 'job_listing_id', 'title', 'description', 'location', 'salary', 'closing_date',
                  'created_at', 'updated_at', 'is_listing_closed', 'positions_available', 'employees',
                  'applicants', 'is_applied']

    def get_is_applied(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            """
            Check if the current user has applied for the job
            """
            return Application.objects.filter(job=obj, applicant=request.user.profile).exists()
        return False

    def get_job_listing_id(self, obj):
        return obj.id


class ApplicationSerializer(serializers.ModelSerializer):
    applicant_username = serializers.CharField(
        source='applicant.user.username', read_only=True)
    job = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all(), write_only=True)

    class Meta:
        model = Application
        fields = ['job', 'employee_status', 'applicant_username']


class ApplicantSerializer(serializers.ModelSerializer):
    applicant = EmployeeProfileSerializer()

    class Meta:
        model = Application
        fields = '__all__'

    def update(self, instance, validated_data):
        employer_applicant_choice = validated_data.get(
            'employer_applicant_choice')
        instance.employer_applicant_choice = employer_applicant_choice
        instance.save()
        return instance


class UpdateApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['employer_applicant_choice']


class EmployeeJobResponseSerializer(serializers.ModelSerializer):
    employee_acceptance_response = serializers.ChoiceField(
        choices=Application.EMPLOYEE_ACCEPTANCE_CHOICES)

    class Meta:
        model = Application
        fields = ['employee_acceptance_response']


class EmployeeJobSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'owner', 'name', 'content', 'image']

    def get_owner(self, obj):
        return obj.owner.username
