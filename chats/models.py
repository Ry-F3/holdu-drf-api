from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    sender = models.ForeignKey(
        User, related_name='sent_chats', on_delete=models.CASCADE)
    recipient = models.ForeignKey(
        User, related_name='received_chats', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Define unique constraint to prevent duplicate messages within the chat list
        unique_together = ['sender', 'recipient', 'timestamp']

    def __str__(self):
        return f'Chat between {self.sender} and {self.recipient}'


class Message(models.Model):
    chat = models.ForeignKey(
        Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(
        User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(
        User, related_name='received_messages', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        # Define unique constraint to prevent duplicate messages within a chat
        unique_together = ['chat', 'sender', 'recipient', 'timestamp']

    def __str__(self):
        return f'Message from {self.sender} in {self.chat}'
