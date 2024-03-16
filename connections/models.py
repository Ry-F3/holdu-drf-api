from django.contrib.auth.models import User
from django.db import models


class Connection(models.Model):
    owner = models.ForeignKey(
        User, related_name='user_connected', on_delete=models.CASCADE)
    connection = models.ForeignKey(
        User, related_name='connections', on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        unique_together = ('owner', 'connection')

    def __str__(self):
        return f"{self.owner} follows {self.connection}"
