from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Chat, Message
from .serializers import ChatSerializer

print('test chats')


class ChatTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', password='password1')
        self.user2 = User.objects.create_user(
            username='user2', password='password2')
        self.client.force_authenticate(user=self.user1)

    def test_create_chat(self):
        url = reverse('chat-list-create')
        data = {'recipient': self.user2.pk, 'content': 'Hello, user2!'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chat.objects.count(), 1)
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(response.data['sender'], self.user1.pk)
        self.assertEqual(response.data['recipient'], self.user2.pk)
        self.assertEqual(response.data['messages']
                         [0]['content'], 'Hello, user2!')

    def test_get_chat_detail(self):
        chat = Chat.objects.create(sender=self.user1, recipient=self.user2)
        Message.objects.create(chat=chat, sender=self.user1,
                               recipient=self.user2, content='Hi, user2!')
        url = reverse('chat-detail', kwargs={'pk': chat.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['sender'], self.user1.pk)
        self.assertEqual(response.data['recipient'], self.user2.pk)
        self.assertEqual(response.data['messages'][0]['content'], 'Hi, user2!')

    def test_invalid_chat_creation(self):
        """
        Test creating a chat without providing recipient
        """
        url = reverse('chat-list-create')
        data = {'content': 'Hello, user2!'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        """
        Test creating a chat with invalid recipient ID
        """
        data = {'recipient': 999, 'content': 'Hello, user2!'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        """
        Test creating a chat with the same user as sender and recipient
        """
        data = {'recipient': self.user1.pk, 'content': 'Hello, user1!'}
        response = self.client.post(url, data, format='json')
        """
        Chat is still valid as most social media platforms
        allow users to send messages to themselves
        """
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_chat(self):
        chat = Chat.objects.create(sender=self.user1, recipient=self.user2)
        url = reverse('chat-detail', kwargs={'pk': chat.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Chat.objects.count(), 0)
