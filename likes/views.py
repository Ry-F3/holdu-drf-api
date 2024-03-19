from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Like
from .serializers import LikeSerializer
from drf_api.permissions import IsOwnerReadOnly


class LikeList(generics.ListCreateAPIView):
    """
    API endpoint that allows likes to be viewed or created.
    Please note: code has been mostly used from CI's walkthrough project.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LikeDetail(generics.RetrieveDestroyAPIView):
    """
    API endpoint that allows likes to be viewed or deleted.
    """
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly, IsOwnerReadOnly]
