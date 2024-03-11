from django.urls import path
from .views import EmployeeProfileView, EmployerProfileView, AdminProfileView
from profiles import views

urlpatterns = [
    path('employee-profiles/', EmployeeProfileView.as_view(),
         name='employee-profiles'),
    path('employee-profiles/<int:pk>/', views.EmployeeProfileDetail.as_view(),
         name='employee-profiles-detail'),
    path('employer-profiles/', EmployerProfileView.as_view(),
         name='employer-profiles'),
    path('employer-profiles/<int:pk>/', views.EmployerProfileDetail.as_view(),
         name='employer-profiles-detail'),
    path('admin-profiles/', AdminProfileView.as_view(), name='admin-profiles'),
    path('admin-profiles/<int:pk>/', views.AdminProfileDetail.as_view(),
         name='admin-profiles-detail'),

]
