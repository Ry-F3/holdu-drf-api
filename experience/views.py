from rest_framework import generics, status
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from .models import WorkExperience
from .serializers import WorkExperienceSerializer
from drf_api.permissions import IsOwnerReadOnly
from rest_framework.permissions import IsAuthenticated


class WorkExperienceListView(generics.ListAPIView):
    """
    Endpoint: GET /work-experience/
    Permission: Authenticated users only.
    Response: List of work experiences.
    """

    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer


class WorkExperienceUserView(ListAPIView):
    """
    Endpoint: GET /work-experience/user/<user_id>/
    Permission: Authenticated users only.
    Response: List of work experiences belonging to the specified user.
    """

    serializer_class = WorkExperienceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the user ID from the URL parameters
        user_id = self.kwargs.get('user_id')

        # Filter work experiences by the specified user ID
        return WorkExperience.objects.filter(owner_id=user_id)


class WorkExperienceCreateView(generics.CreateAPIView):
    """
    Endpoint: POST /work-experience/create
    Permission: Authenticated users only, owner.
    Response: New work experience created.
    """

    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer
    permission_classes = [IsAuthenticated, IsOwnerReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"message": "Work experience created successfully.", "data": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def perform_create(self, serializer):
        """Save new work experience."""
        serializer.save(owner=self.request.user)


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
