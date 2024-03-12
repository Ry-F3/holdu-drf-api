from rest_framework import generics, permissions, status, serializers
from django.http import Http404
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer
from drf_api.permissions import IsOwnerReadOnly, IsEmployerProfile, IsEmployeeProfile, IsApplicant


class JobListView(generics.ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]


class JobPostView(generics.CreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployerProfile]

    def perform_create(self, serializer):
        serializer.save(employer_profile=self.request.user.profile)


class JobDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerReadOnly]

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            """ 
            Check if the user is an employer to allow editing and deletion 
            """
            return [IsEmployerProfile()]
        return super().get_permissions()


class ApplyJobView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsEmployeeProfile, IsApplicant]

    def perform_create(self, serializer):
        try:
            job_id = self.kwargs.get('pk')
            job = get_object_or_404(Job, id=job_id)
            applicant_profile = self.request.user.profile

            existing_application = Application.objects.filter(
                job=job, applicant=applicant_profile).first()

            if existing_application:
                """ 
                User has already applied, return a response without creating a new application 
                """
                serializer = self.get_serializer(existing_application, context={
                                                 'request': self.request})
                data = serializer.data
                raise serializers.ValidationError(
                    {"detail": "You have already applied for this job.", "data": data})

            """
            Automatically set the applicant and job based on the current user's profile and the job_id
            """
            serializer.save(applicant=applicant_profile, job=job)
        except Job.DoesNotExist:
            raise Http404("Job not found")

    def get(self, request, *args, **kwargs):
        try:
            job_id = self.kwargs.get('pk')
            job = get_object_or_404(Job, id=job_id)

            is_applied = Application.objects.filter(
                job=job, applicant=request.user.profile).exists()

            if is_applied:
                """ 
                If the user has already applied, return a response indicating the application status
                """
                serializer = JobSerializer(
                    job, context={'request': self.request})
                return Response(serializer.data)

            """ 
            If the user hasn't applied, return a response with status 400 indicating that they haven't applied 
            """
            return Response({"detail": "You haven't applied for this job yet."}, status=status.HTTP_400_BAD_REQUEST)

        except Job.DoesNotExist:
            raise Http404("Job not found")


class UnapplyJobView(generics.DestroyAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsEmployeeProfile, IsApplicant]

    def get_object(self):
        try:
            job_id = self.kwargs.get('pk')
            job = get_object_or_404(Job, id=job_id)
            applicant_profile = self.request.user.profile
            return get_object_or_404(Application, job=job, applicant=applicant_profile)

        except Job.DoesNotExist:
            raise Http404("Job not found")

    def delete(self, request, *args, **kwargs):
        try:
            application = self.get_object()

            if Application.objects.filter(job=application.job, applicant=application.applicant).exists():
                """ 
                Serialize the application before deleting it
                """
                serializer = self.get_serializer(
                    application, context={'request': self.request})
                data = serializer.data

                """ 
                Delete the application
                """
                application.delete()

                return Response({"detail": "You have successfully unapplied from this job.", "data": data},
                                status=status.HTTP_200_OK)
            else:
                raise Http404("You haven't applied for this job.")
        except Job.DoesNotExist:
            raise Http404("Job not found")
