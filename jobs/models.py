from django.db import models
from profiles.models import Profile


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    employer_profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='jobs_created', limit_choices_to={'profile_type': 'employer'}
    )
    closing_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    """
    Fields for managing positions
    """
    positions_available = models.PositiveIntegerField(
        default=1, help_text='Number of positions available')

    """
    Fields for managing applicants
    """
    applicants = models.ManyToManyField(
        Profile, through='Application', related_name='job_applications', blank=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Job {self.id} - {self.title} by {self.employer_profile.owner.username}"


class Application(models.Model):
    APPLICANT_STATUS_CHOICES = (
        ('applied', 'Applied'),
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(
        Profile, on_delete=models.CASCADE, limit_choices_to={
            'profile_type': 'employee'}
    )
    status = models.CharField(
        max_length=20, choices=APPLICANT_STATUS_CHOICES, default='pending')

    class Meta:
        """
        Ensure each applicant can only apply once to a job
        """
        unique_together = ('job', 'applicant')

    def __str__(self):
        return f"{self.applicant} - {self.job}: {self.get_status_display()}"
