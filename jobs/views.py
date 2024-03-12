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

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return JobSerializer
        """ 
        Serializer for job details without the form fields 
        """
        return self.serializer_class
        """ 
        Use the default serializer for other methods 
        """

    def perform_create(self, serializer):
        job_id = self.kwargs.get('pk')
        job = get_object_or_404(Job, id=job_id)
        applicant_profile = self.request.user.profile

        """ 
        Check if the user has already applied for the job 
        """
        existing_application = Application.objects.filter(
            job=job, applicant=applicant_profile
        ).first()

        if existing_application:
            """ 
            User has already applied, return a response without creating a new application 
            """
            serializer = self.get_serializer(
                existing_application, context={'request': request})
            data = serializer.data
            return Response(
                {"detail": "You have already applied for this job.", "data": data},
                status=status.HTTP_400_BAD_REQUEST
            )

        """ 
        Automatically set the applicant and job based on the current user's profile and the job_id 
        """
        serializer.save(applicant=applicant_profile, job=job)

    def get(self, request, *args, **kwargs):
        job_id = self.kwargs.get('pk')
        job = get_object_or_404(Job, id=job_id)

        # Check if the user has applied for the job
        is_applied = Application.objects.filter(
            job=job, applicant=self.request.user.profile
        ).exists()

        if is_applied:
            # If the user has already applied, return a response indicating the application status
            serializer = JobSerializer(job, context={'request': request})
            return Response(serializer.data)

        """ 
        If the user hasn't applied, return a response with status 400 indicating that they haven't applied
        """
        return Response(
            {"detail": "You haven't applied for this job yet."},
            status=status.HTTP_400_BAD_REQUEST
        )


class UnapplyJobView(generics.DestroyAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated,
                          IsEmployeeProfile, IsApplicant]

    def get_object(self):
        job_id = self.kwargs.get('pk')
        job = get_object_or_404(Job, id=job_id)
        applicant_profile = self.request.user.profile
        return get_object_or_404(Application, job=job, applicant=applicant_profile)

    def delete(self, request, *args, **kwargs):
        application = self.get_object()

        """ 
        Check if the user has applied for the job 
        """
        if Application.objects.filter(
            job=application.job, applicant=application.applicant
        ).exists():
            """ 
            Serialize the application before deleting it 
            """
            serializer = self.get_serializer(
                application, context={'request': request})
            data = serializer.data

            """ 
            Delete the application 
            """
            application.delete()

            return Response(
                {"detail": "You have successfully unapplied from this job.", "data": data},
                status=status.HTTP_200_OK
            )
        else:
            """ 
            User hasn't applied, return a forbidden response
            """
            raise Http404("You haven't applied for this job.")
