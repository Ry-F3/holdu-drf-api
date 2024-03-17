from django.urls import path
from .views import ChatListCreateAPIView, ChatDetailAPIView

urlpatterns = [
    path('chats/', ChatListCreateAPIView.as_view(), name='chat-list-create'),
    path('chats/<int:pk>/', ChatDetailAPIView.as_view(), name='chat-detail'),
]
