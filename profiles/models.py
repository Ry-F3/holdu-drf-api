from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    PROFILE_CHOICES = (
        ('employee', 'Employee'),
        ('employer', 'Employer'),
    )

    owner = models.OneToOneField(
        User, on_delete=models.CASCADE)
    profile_type = models.CharField(max_length=10, choices=PROFILE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_wyamnj')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"
