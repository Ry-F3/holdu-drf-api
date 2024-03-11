from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from rest_framework.permissions import IsAuthenticated
from .serializers import EmployeeProfileSerializer, EmployerProfileSerializer, AdminProfileSerializer


class EmployeeProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles_employee = Profile.objects.filter(profile_type='employee')
        serializer = EmployeeProfileSerializer(profiles_employee, many=True)

        return Response(serializer.data)


class EmployerProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles_employer = Profile.objects.filter(profile_type='employer')
        serializer = EmployerProfileSerializer(profiles_employer, many=True)

        return Response(serializer.data)


class AdminProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles_admin = Profile.objects.filter(profile_type='admin')
        serializer = AdminProfileSerializer(profiles_admin, many=True)

        return Response(serializer.data)
