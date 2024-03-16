from django.urls import path
from connections import views

urlpatterns = [
    path('connections/', views.ConnectionList.as_view(), name='connection-list'),
    path('connections/<int:pk>/', views.ConnectionDetail.as_view(),
         name='connection-detail'),
    path('accepted-connections/', views.AcceptedConnectionList.as_view(),
         name='accepted-connection-list'),
    path('pending-connections/', views.PendingConnectionList.as_view(),
         name='pending-connection-list'),
    path('pending-connections/<int:pk>/accept/',
         views.AcceptConnection.as_view(), name='accept-connection'),
    path('pending-connections/<int:pk>/decline/',
         views.DeclineConnection.as_view(), name='decline-connection'),
]
