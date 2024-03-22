from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import Connection


class ConnectionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='user1', password='password1')
        self.user2 = User.objects.create_user(
            username='user2', password='password2')

    def test_create_connection_with_invalid_data(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('connection-list')
        """
        Omitting the 'connection' field to simulate invalid data 
        """
        data = {}
        response = self.client.post(url, data, format='json')
        """
        Expect a 400 Bad Request response
        """
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        """ 
        Ensure that no connection is created 
        """
        self.assertFalse(Connection.objects.filter(
            owner=self.user1, connection=self.user2).exists())

    def test_create_connection_with_valid_data(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('connection-list')
        data = {'connection': self.user2.id}  # Provide valid data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Connection.objects.filter(
            owner=self.user1, connection=self.user2).exists())

    def test_accept_connection(self):
        self.client.force_authenticate(user=self.user1)
        connection = Connection.objects.create(
            owner=self.user2, connection=self.user1)
        url = reverse('accept-connection', kwargs={'pk': connection.pk})
        response = self.client.put(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        connection.refresh_from_db()
        self.assertTrue(connection.accepted)

    def test_decline_connection(self):
        self.client.force_authenticate(user=self.user1)
        connection = Connection.objects.create(
            owner=self.user2, connection=self.user1)
        url = reverse('decline-connection', kwargs={'pk': connection.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Connection.objects.filter(
            owner=self.user2, connection=self.user1).exists())

    def test_delete_connection(self):
        self.client.force_authenticate(user=self.user1)
        connection = Connection.objects.create(
            owner=self.user1, connection=self.user2)
        url = reverse('connection-detail', kwargs={'pk': connection.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Connection.objects.filter(
            owner=self.user1, connection=self.user2).exists())


def test_get_accepted_connections(self):
    self.client.force_authenticate(user=self.user1)
    url = reverse('accepted-connection-list')
    response = self.client.get(url)

    self.assertEqual(response.status_code, status.HTTP_200_OK)
    """
    Assert based on the actual number of accepted connections
    """
    self.assertEqual(len(response.data),
                     Connection.objects.filter(accepted=True).count())


def test_get_pending_connections(self):
    self.client.force_authenticate(user=self.user1)
    url = reverse('pending-connection-list')
    response = self.client.get(url)
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    """
    Assert based on the actual number of pending connections
    """
    self.assertEqual(len(response.data),
                     Connection.objects.filter(accepted=False).count())
