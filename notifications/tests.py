from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Notification
from profiles.models import Profile, Rating
from connections.models import Connection
from jobs.models import Job
from chats.models import Message, Chat
from likes.models import Like
from comments.models import Comment
from datetime import datetime, timedelta
from django.utils import timezone


class NotificationSignalTest(APITestCase):
    """Tests for notification creation signals."""

    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1", password="testpassword"
        )
        self.user2 = User.objects.create_user(
            username="testuser2", password="testpassword"
        )
        self.profile = Profile.objects.create(
            owner=self.user2, profile_type='employee')

        closing_date = timezone.now()

        self.job = Job.objects.create(
            employer_profile=self.profile,
            title="Test Job",
            description="Test Job Description",
            closing_date=closing_date + timedelta(days=10)
        )

        print(f"\n{self.id()}")

    def test_notification_created_for_new_connection_accepted(self):
        connection = Connection.objects.create(
            owner=self.user1, connection=self.user2, accepted=True)
        notification1 = Notification.objects.get(
            owner=self.user1, category='connection_accepted')
        notification2 = Notification.objects.get(
            owner=self.user2, category='connection_accepted')

        self.assertEqual(notification1.title, "You have a new Connection!")
        self.assertEqual(notification1.sender, self.user1)
        self.assertEqual(notification1.content,
                         f'You are now connected to {self.user2.username}.')
        self.assertEqual(notification1.item_id, connection.id)

        self.assertEqual(
            notification2.title, f"Connection request accepted by {self.user1.username}!")
        self.assertEqual(notification2.sender, self.user1)
        self.assertEqual(notification2.content,
                         f'Your connection request to {self.user1.username} has been accepted.')
        self.assertEqual(notification2.item_id, connection.id)

    def test_notification_created_for_new_connection_request(self):
        connection = Connection.objects.create(
            owner=self.user1, connection=self.user2, accepted=False)
        notification = Notification.objects.get(
            owner=self.user2, category='connection_request')

        self.assertEqual(
            notification.title, f"You have a new Connection request from {self.user1.username}!")
        self.assertEqual(notification.sender, self.user1)
        self.assertEqual(notification.content,
                         f'{self.user1.username} sent you a connection request.')
        self.assertEqual(notification.item_id, connection.id)

    def test_notification_created_for_new_message(self):
        """
        Create a Chat instance 
        """
        chat = Chat.objects.create(sender=self.user1, recipient=self.user2)
        """ 
        Create a Message instance with chat_id 
        """
        message = Message.objects.create(
            chat=chat,
            sender=self.user1,
            recipient=self.user2,
            content="Test message"
        )
        notification = Notification.objects.get(
            owner=self.user2, category='message_alert')

        self.assertEqual(notification.title, "New Message")
        self.assertEqual(notification.sender, self.user1)
        self.assertEqual(
            notification.content, f'You have received a new message from {self.user1.username}.')
        self.assertEqual(notification.item_id, message.id)

    def test_notification_created_for_new_job(self):
        """ 
        Trigger the signal by creating a new Job instance
        """
        notification_count_before = Notification.objects.count()
        """ 
        Create a new Job instance
        """
        closing_date = timezone.now() + timedelta(days=10)
        """ 
        Create a new Job instance 
        """
        job = Job.objects.create(
            employer_profile=self.profile,
            title="Test Job 2",
            description="Test Job Description 2",
            closing_date=closing_date
        )
        notification_count_after = Notification.objects.count()
        """
        Check if a new notification was created 
        """
        self.assertEqual(notification_count_after,
                         notification_count_before + 1)

    def test_notification_created_for_new_rating(self):
        rating = Rating.objects.create(
            rate_user=self.user1, created_by=self.user2, rating=5)
        notification = Notification.objects.get(
            owner=self.user1, category='new_rating')

        self.assertEqual(notification.title, "New Rating")
        self.assertEqual(notification.sender, self.user2)
        self.assertEqual(
            notification.content, f"You have received a new rating from {self.user2.username}.")
        self.assertEqual(notification.item_id, rating.id)
