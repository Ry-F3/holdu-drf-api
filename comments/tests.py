from django.utils import timezone
from profiles.models import Profile
from jobs.models import Job
from .models import Comment
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth.models import User

print('test comments')


class CommentTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        """ 
        Create a Profile instance for the user with profile_type set to 'employer'
        """
        profile = Profile.objects.create(
            owner=self.user, profile_type='employer')
        """
        Create a Job instance with required fields
        """
        self.job = Job.objects.create(
            title="Test Job",
            description="Test Description",
            closing_date=timezone.now() + timezone.timedelta(days=7),
            employer_profile=profile  # Associate the job with the employer profile
        )

    def test_create_comment(self):
        url = reverse('comment-list')
        data = {
            'owner': self.user.id,
            'job': self.job.id,
            'content': 'Test Comment Content'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.get().content, 'Test Comment Content')

    def test_get_comment_detail(self):
        comment = Comment.objects.create(
            owner=self.user, job=self.job, content='Test Comment Content')
        url = reverse('comment-detail', kwargs={'pk': comment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['content'], 'Test Comment Content')

    def test_update_comment(self):
        comment = Comment.objects.create(
            owner=self.user, job=self.job, content='Original Content')
        url = reverse('comment-detail', kwargs={'pk': comment.pk})
        updated_data = {'content': 'Updated Content'}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.get(
            pk=comment.pk).content, 'Updated Content')

    def test_delete_comment(self):
        comment = Comment.objects.create(
            owner=self.user, job=self.job, content='Test Comment Content')
        url = reverse('comment-detail', kwargs={'pk': comment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)
