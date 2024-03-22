from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from profiles.models import Profile
from experience.models import WorkExperience
from datetime import date

print("Experience")


class WorkExperienceTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        """ 
        Create Profile for the user 
        """
        profile = Profile.objects.create(
            owner=self.user, profile_type='employee')

        self.client.force_authenticate(user=self.user)

        """ 
        Create work experiences
        """
        self.work_experience1 = WorkExperience.objects.create(
            owner=self.user,  # Using user instance as owner
            job_title='Software Engineer',
            company_name='ABC Technologies',
            start_date=date(2019, 1, 1),
            end_date=date(2022, 1, 1),
            skills='Python, Django, JavaScript',
            job_summary='Worked on web development projects.'
        )
        self.work_experience2 = WorkExperience.objects.create(
            owner=self.user,  # Using user instance as owner
            job_title='Data Analyst',
            company_name='XYZ Corporation',
            start_date=date(2022, 1, 1),
            end_date=None,  # Still working
            skills='Data analysis, SQL, Python',
            job_summary='Analyzing large datasets.'
        )

    def test_work_experience_list(self):
        url = reverse('work_experience_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), WorkExperience.objects.count())

    def test_work_experience_detail(self):
        url = reverse('work_experience_detail',
                      kwargs={'pk': self.work_experience1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['job_title'],
                         self.work_experience1.job_title)

    def test_work_experience_create(self):
        url = reverse('work_experience_create')
        data = {
            'job_title': 'Software Developer',
            'company_name': 'PQR Solutions',
            'start_date': '2022-01-01',
            'end_date': '2023-12-31',
            'skills': 'Java, Spring Boot',
            'job_summary': 'Developing software applications.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WorkExperience.objects.count(), 3)

    def test_work_experience_edit(self):
        url = reverse('work_experience_detail',
                      kwargs={'pk': self.work_experience2.pk})
        data = {
            'job_title': 'Data Scientist',
            'company_name': 'ABC Corporation',
            'start_date': '2022-01-01',
            'end_date': None,  # Still working
            'skills': 'Machine Learning, Python',
            'job_summary': 'Building predictive models.'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['job_title'], 'Data Scientist')

    def test_work_experience_delete(self):
        url = reverse('work_experience_detail',
                      kwargs={'pk': self.work_experience2.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(WorkExperience.objects.count(), 1)
