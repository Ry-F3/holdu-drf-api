from django.test import TestCase
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from jobs.models import Job
from profiles.models import Profile
from .models import Like
from django.utils import timezone

print('test likes')


class LikeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        """
        Create a Profile instance for the user
        """
        profile = Profile.objects.create(
            profile_type='employer', owner=self.user)

        self.client.force_authenticate(user=self.user)
        self.job = Job.objects.create(
            title='Test Job',
            description='This is a test job',
            location='Test location',
            salary=50000,
            employer_profile=profile,
            closing_date=timezone.now()
        )

    def test_like_create(self):
        url = reverse('like-list')
        data = {'job': self.job.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(),
                         Like.objects.filter(owner=self.user).count())
        self.assertEqual(Like.objects.get().owner, self.user)

    def test_like_list(self):
        Like.objects.create(owner=self.user, job=self.job)
        url = reverse('like-list')
        response = self.client.get(url, format='josn')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_like_detail(self):
        like = Like.objects.create(owner=self.user, job=self.job)
        url = reverse('like-detail', kwargs={'pk': like.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_like_delete(self):
        like = Like.objects.create(owner=self.user, job=self.job)
        url = reverse('like-detail', kwargs={'pk': like.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Like.objects.count(),
                         Like.objects.filter(owner=self.user).count())
