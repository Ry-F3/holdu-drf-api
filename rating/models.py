from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
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
    average_rating = models.FloatField(default=0)

    def __str__(self):
        return f"Rating of {self.rating} given by {self.rating_user} to {self.rated_user}"

    def save(self, *args, **kwargs):
        # Calculate the average rating for the rated user
        average_rating = Rating.objects.filter(
            rated_user=self.rated_user).aggregate(Avg('rating'))['rating__avg']
        if average_rating is not None:
            self.rated_user.average_rating = average_rating
        else:
            self.rated_user.average_rating = 0  # Set default if no ratings
        self.rated_user.save()  # Save the rated user instance
        super().save(*args, **kwargs)  # Call the parent class's save method
