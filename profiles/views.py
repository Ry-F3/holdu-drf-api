from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from rest_framework.permissions import IsAuthenticated
from .serializers import EmployeeProfileSerializer, EmployerProfileSerializer, AdminProfileSerializer


class EmployeeProfileView(APIView):
    """
    Employee Profile view.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles_employee = Profile.objects.filter(profile_type='employee')
        serializer = EmployeeProfileSerializer(profiles_employee, many=True)

        return Response(serializer.data)


class EmployeeProfileDetail(APIView):
    """
    Employee Profile get by id, if id does not exist return a http 404 error.
    """

    def get_object(self, pk):
        try:
            employeeProfile = Profile.objects.get(
                profile_type='employee', pk=pk)
            return employeeProfile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        employeeProfile = self.get_object(pk)
        serializer = EmployeeProfileSerializer(employeeProfile)
        return Response(serializer.data)


class EmployerProfileView(APIView):
    """
    Employer Profile view.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles_employer = Profile.objects.filter(profile_type='employer')
        serializer = EmployerProfileSerializer(profiles_employer, many=True)

        return Response(serializer.data)


class EmployerProfileDetail(APIView):
    """
    Employer Profile get by id, if id does not exist return a http 404 error.
    """

    def get_object(self, pk):
        try:
            employerProfile = Profile.objects.get(
                profile_type='employer', pk=pk)
            return employerProfile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        employerProfile = self.get_object(pk)
        serializer = EmployerProfileSerializer(employerProfile)
        return Response(serializer.data)


class AdminProfileView(APIView):
    """
    Admin Profile view.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles_admin = Profile.objects.filter(profile_type='admin')
        serializer = AdminProfileSerializer(profiles_admin, many=True)

        return Response(serializer.data)


class AdminProfileDetail(APIView):
    """
    Admin Profile get by id, if id does not exist return a http 404 error.
    """

    def get_object(self, pk):
        try:
            adminProfile = Profile.objects.get(profile_type='admin', pk=pk)
            return adminProfile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        adminProfile = self.get_object(pk)
        serializer = AdminProfileSerializer(adminProfile)
        return Response(serializer.data)
