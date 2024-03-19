from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job


class Like(models.Model):
    """
    Like model, related to 'owner' and 'job'.
    Please note: code has been mostly used from CI's walkthrough project.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(
        Job, related_name='likes', on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['owner', 'job']

    def __str__(self):
        return f'{self.owner} {self.job}'
