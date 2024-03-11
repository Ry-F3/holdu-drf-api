from django.urls import path
from .views import EmployeeProfileView, EmployerProfileView, AdminProfileView

urlpatterns = [
    path('employee-profiles/', EmployeeProfileView.as_view(),
         name='employee-profiles'),
    path('employer-profiles/', EmployerProfileView.as_view(),
         name='employer-profiles'),
    path('admin-profiles/', AdminProfileView.as_view(), name='admin-profiles'),

]
