from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):
    CATEGORIES = [
        ('connection', 'Connection'),
        ('new_job', 'New Job'),
        ('accepted_application', 'Accepted Application'),
        ('message_alert', 'Message Alert'),
        ('connection_request', 'Connection_Request'),
    ]

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    sent_at = models.DateTimeField(auto_now_add=True)
    category = models.CharField(choices=CATEGORIES, max_length=50)
    is_read = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=255)
    item_id = models.IntegerField()

    class Meta:
        ordering = ['-sent_at']

    def __str__(self):
        return f"{self.category} notification for {self.owner}"
