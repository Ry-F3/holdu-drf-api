from django.urls import path
from .views import (
    JobListView,
    JobDetailView,
    ApplyJobView,
    JobPostView,
    UnapplyJobView,
    ApplicantListView,
    ApplicantDetailView,
)

urlpatterns = [
    path('jobs/', JobListView.as_view(), name='job-list'),
    path('jobs/post/', JobPostView.as_view(), name='job-post'),
    path('jobs/post/<int:pk>/', JobDetailView.as_view(), name='job-detail'),

    path('jobs/post/<int:pk>/apply/', ApplyJobView.as_view(), name='apply-job'),
    path('jobs/post/<int:pk>/unapply/',
         UnapplyJobView.as_view(), name='unapply-job'),
    path('jobs/post/<int:pk>/applicants/',
         ApplicantListView.as_view(), name='applicant-list'),
    path('jobs/post/<int:pk>/applicants/<int:applicant_id>/',
         ApplicantDetailView.as_view(), name='applicant-detail'),


]
