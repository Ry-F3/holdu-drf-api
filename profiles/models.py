from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver


class Profile(models.Model):
    PROFILE_CHOICES = (
        ('employee', 'Employee'),
        ('employer', 'Employer'),
        ('admin', 'Admin'),
    )

    owner = models.OneToOneField(
        User, on_delete=models.CASCADE)
    profile_type = models.CharField(
        max_length=10, choices=PROFILE_CHOICES, default='admin')
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


def new_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance)


post_save.connect(new_profile, sender=User)
