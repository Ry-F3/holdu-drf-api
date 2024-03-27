from django.urls import path
from profiles import views
from .views import (
    ProfilesView, ProfileDetailView, RateUserView, ProfileRatingAPIView,
    RatingEditAPIView, MyLoginView
)

urlpatterns = [
    path('login/', MyLoginView.as_view(), name='login'),
    path('profiles/', ProfilesView.as_view(), name='profiles'),
    path('profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profiles/<int:pk>/rate-user/',
         RateUserView.as_view(), name='rate-user'),
    path('profiles/<int:pk>/ratings/',
         ProfileRatingAPIView.as_view(), name='profile-rating'),
    path('profiles/<int:pk>/ratings-edit',
         RatingEditAPIView.as_view(), name='ratings-edit'),

]
