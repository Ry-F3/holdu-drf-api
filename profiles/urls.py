from django.urls import path
from profiles import views
from .views import (
    EmployeeProfileView, EmployerProfileView, AdminProfileView,
    ProfilesView, RateUserView, ProfileRatingAPIView,
    RatingEditAPIView
)

urlpatterns = [
    path('profiles/', ProfilesView.as_view(), name='profiles'),
    path('profiles/<int:pk>/rate-user/',
         RateUserView.as_view(), name='rate-user'),
    path('profiles/<int:pk>/ratings/',
         ProfileRatingAPIView.as_view(), name='profile-rating'),
    path('profiles/<int:pk>/ratings-edit',
         RatingEditAPIView.as_view(), name='ratings-edit'),
    path('profiles/employee/', EmployeeProfileView.as_view(),
         name='employee'),
    path('profiles/employee/<int:pk>/', views.EmployeeProfileDetail.as_view(),
         name='employee-detail'),
    path('profiles/employer/', EmployerProfileView.as_view(),
         name='employer'),
    path('profiles/employer/<int:pk>/', views.EmployerProfileDetail.as_view(),
         name='employer-detail'),
    path('profiles/admin/', AdminProfileView.as_view(), name='admin'),
    path('profiles/admin/<int:pk>/', views.AdminProfileDetail.as_view(),
         name='admin-detail'),

]
