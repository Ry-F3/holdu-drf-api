from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job


class Comment(models.Model):
    """
    Comment model, related to User and Job 
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content
