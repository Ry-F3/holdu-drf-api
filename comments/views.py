from rest_framework import generics, permissions
from drf_api.permissions import IsOwnerReadOnly
from .models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer


class CommentList(generics.ListCreateAPIView):
    """
    Comment List view, allowing users to post comments relating to Jobs.
    Please note: code has been mostly used from CI's walkthrough project.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerReadOnly]
    serializer_class = CommentDetailSerializer
    queryset = Comment.objects.all()
