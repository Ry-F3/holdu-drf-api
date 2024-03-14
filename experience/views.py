from rest_framework import generics, status
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import WorkExperience
from .serializers import WorkExperienceSerializer
from drf_api.permissions import IsOwnerReadOnly
from rest_framework.permissions import IsAuthenticated


class WorkExperienceListView(ListAPIView):
    """
    Endpoint: GET /work-experience/
    Permission: Authenticated users only.
    Response: List of work experiences belonging to the authenticated user.
    """

    serializer_class = WorkExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return WorkExperience.objects.filter(owner=user)


class WorkExperienceCreateView(generics.CreateAPIView):
    """
    Endpoint: POST /work-experience/create
    Permission: Authenticated users only, owner.
    Response: New work experience created.
    """

    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    permission_classes = [IsAuthenticated, IsOwnerReadOnly]

    def perform_create(self, serializer):
        """Save new work experience."""
        try:
            serializer.save(owner=self.request.user)
            return Response({"message": "Work experience created successfully.", "data": WorkExperienceSerializer(instance).data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WorkExperienceEditView(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint: GET /work-experience/create/{id}/, PUT/PATCH /work-experience/create/{id}/, DELETE /work-experience/create/{id}/
    Permission: Authenticated users only, owner.
    Response: Retrieve/Update/Delete work experience.
    """

    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    permission_classes = [IsAuthenticated, IsOwnerReadOnly]

    def perform_update(self, serializer):
        """Update work experience."""
        try:
            instance = serializer.save()
            return Response({"message": "Work experience updated successfully.", "data": WorkExperienceSerializer(instance).data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_destroy(self, instance):
        """Delete work experience."""
        try:
            instance.delete()
            return Response({"message": "Work experience deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
