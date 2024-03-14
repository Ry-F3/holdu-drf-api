from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job
from profiles.models import Profile


class WorkExperience(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    skills = models.TextField(blank=True)
    job_summary = models.TextField(blank=True)

    class Meta:
        unique_together = ['job_title', 'company_name',
                           'start_date', 'end_date', 'skills', 'job_summary', 'owner']
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.profile.owner}'s Work Experience at {self.company_name}"

    def save(self, *args, **kwargs):
        try:
            profile = self.owner.profile
            if profile.profile_type != 'employee':
                raise ValueError(
                    "Work experiences can only be created for profiles with 'employee' profile type.")
        except Profile.DoesNotExist:
            raise ValueError(
                "Work experiences can only be created for users with associated profiles.")
        super().save(*args, **kwargs)
