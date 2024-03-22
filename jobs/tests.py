from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from jobs.models import Job, Application
from profiles.models import Profile
from django.utils import timezone
from datetime import timedelta

print('test jobs')


class JobApplicationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.employer_user = User.objects.create_user(
            username='employer', password='testpassword'
        )
        self.employee_user = User.objects.create_user(
            username='employee', password='testpassword'
        )
        self.employer_profile = Profile.objects.create(
            owner=self.employer_user, profile_type='employer'
        )
        self.employee_profile = Profile.objects.create(
            owner=self.employee_user, profile_type='employee'
        )
        self.job = Job.objects.create(
            employer_profile=self.employer_profile,
            title="Test Job",
            description="Test Job Description",
            closing_date=timezone.now() + timedelta(days=5)
        )

    def test_apply_job(self):
        url = reverse('apply-job', kwargs={'pk': self.job.pk})
        self.client.force_login(self.employee_user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_apply_job_listing_closed(self):
        self.job.closing_date = timezone.now() - timedelta(days=1)
        self.job.save()
        url = reverse('apply-job', kwargs={'pk': self.job.pk})
        self.client.force_login(self.employee_user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unapply_job(self):
        application = Application.objects.create(
            job=self.job, applicant=self.employee_profile
        )
        url = reverse('unapply-job', kwargs={'pk': self.job.pk})
        self.client.force_login(self.employee_user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Application.objects.filter(
            job=self.job, applicant=self.employee_profile).exists())
