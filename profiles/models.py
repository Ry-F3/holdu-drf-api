from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    PROFILE_CHOICES = (
        ('employee', 'Employee'),
        ('employer', 'Employer'),
        ('admin', 'Admin'),
    )

    owner = models.OneToOneField(
        User, on_delete=models.CASCADE)
    profile_type = models.CharField(
        max_length=10, choices=PROFILE_CHOICES, default='', blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255, blank=True)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_profile_wyamnj')
    ratings = models.ManyToManyField(
        'Rating', related_name='profiles', blank=True)
    average_rating = models.FloatField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner}'s profile"


class Rating(models.Model):
    RATINGS_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    rating = models.IntegerField(choices=RATINGS_CHOICES, default=1)
    comment = models.TextField(blank=True)
    rate_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Rating: {self.rating}"


def new_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            profile_type = 'employee'  # Set the default profile type for superusers
        else:
            # Use the provided profile_type for non-superusers
            profile_type = instance.profile_type

        print(
            f"Creating profile for user {instance.username} with profile type: {profile_type}")
        Profile.objects.create(owner=instance, profile_type=profile_type)


post_save.connect(new_profile, sender=User)
