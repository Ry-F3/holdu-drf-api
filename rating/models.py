from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job


class Rating(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    rated_user = models.ForeignKey(
        User, related_name='ratings_received', on_delete=models.CASCADE)
    rating_user = models.ForeignKey(
        User, related_name='ratings_given', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, choices=[(
        i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"Rating of {self.rating} given by {self.rating_user} to {self.rated_user}"
