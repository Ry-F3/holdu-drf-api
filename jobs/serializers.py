from rest_framework import serializers
from .models import Job, Application
from profiles.serializers import BaseProfileSerializer, EmployeeProfileSerializer, EmployerProfileSerializer


class JobSerializer(serializers.ModelSerializer):
    employer_profile = EmployerProfileSerializer(read_only=True)
    applicants = BaseProfileSerializer(many=True, read_only=True)
    is_applied = serializers.SerializerMethodField(default=False)
    job_listing_id = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ['employer_profile', 'job_listing_id', 'title', 'description', 'location', 'salary', 'closing_date',
                  'created_at', 'updated_at', 'positions_available', 'applicants', 'is_applied']

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
    applicant = serializers.StringRelatedField(
        source='applicant.user.username', read_only=True)
    job = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.all(), write_only=True)

    class Meta:
        model = Application
        fields = '__all__'
