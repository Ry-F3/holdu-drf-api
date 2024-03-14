from django.urls import path
from .views import (
    WorkExperienceListView,
    WorkExperienceCreateView,
    WorkExperienceEditView,
    WorkExperienceUserView,
)

urlpatterns = [
    path('work-experience/', WorkExperienceListView.as_view(),
         name='work_experience_list'),
    path('work-experience/user/<int:user_id>/',
         WorkExperienceUserView.as_view(), name='user_work_experience'),
    path('work-experience/create', WorkExperienceCreateView.as_view(),
         name='work_experience_create'),
    path('work-experience/create/<int:pk>/', WorkExperienceEditView.as_view(),
         name='work_experience_detail'),
]
