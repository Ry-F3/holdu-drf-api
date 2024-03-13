from django.db import models
from profiles.models import Profile
from django.utils import timezone


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=100)
    salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    employer_profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='jobs_created', limit_choices_to={'profile_type': 'employer'}
    )
    employees = models.ManyToManyField(
        Profile, related_name='assigned_jobs',
        limit_choices_to={'profile_type': 'employee'},
        blank=True
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
    is_listing_closed = models.BooleanField(default=False)

    def close_listing(self):
        self.is_listing_closed = True
        self.save()

    def reopen_listing(self):
        self.is_listing_closed = False
        self.save()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Job {self.id} - {self.title} by {self.employer_profile.owner.username}"


class Application(models.Model):
    EMPLOYEE_STATUS_CHOICES = (
        ('applied', 'Applied'),
    )

    EMPLOYER_APPLICANT_STATUS_CHOICES = (
        ('binned', 'Binned'),
        ('shortlisted', 'Shortlisted'),
        ('accepted', 'Accepted')
    )

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    applicant = models.ForeignKey(
        Profile, on_delete=models.CASCADE, limit_choices_to={
            'profile_type': 'employee'}
    )
    employee_status = models.CharField(
        max_length=20, choices=EMPLOYEE_STATUS_CHOICES, default='applied'
    )
    employer_applicant_choice = models.CharField(
        max_length=20, choices=EMPLOYER_APPLICANT_STATUS_CHOICES, default='pending'
    )

    class Meta:
        """
        Ensure each applicant can only apply once to a job
        """
        unique_together = ('job', 'applicant')

    def __str__(self):
        return f"{self.applicant} - {self.job}: {self.get_employee_status_display()} - {self.get_employer_applicant_status_display()}"
