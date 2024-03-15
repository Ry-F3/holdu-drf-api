from django.http import Http404
from rest_framework.exceptions import NotFound, PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import status, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile, Rating
from rest_framework.permissions import IsAuthenticated
from drf_api.permissions import IsOwnerReadOnly, IsRatingCreator
from django.db.models import Avg
from rest_framework.generics import (
    CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView,
    UpdateAPIView, DestroyAPIView
)
from .serializers import (
    EmployeeProfileSerializer, EmployerProfileSerializer, RateUserSerializer,
    BaseProfileSerializer, AdminProfileSerializer, RatingSerializer,
    BaseProfileSerializer
)


class ProfilesView(generics.ListAPIView):
    """
    View to retrieve all profiles.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BaseProfileSerializer
    queryset = Profile.objects.all()

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter
    ]

    search_fields = [
        'owner__username',
        'average_rating',
        'created_at',
        'profile_type',
    ]

    ordering_fields = [
        'owner__username',
        'average_rating',
        'created_at',
        'profile_type',
    ]

    def get(self, request, *args, **kwargs):
        """ Get the queryset based on search and ordering """
        queryset = self.filter_queryset(self.get_queryset())

        """ Serialize the queryset using the serializer class """
        serializer = self.serializer_class(
            queryset, many=True, context={'request': request})

        """ Return the serialized data in JSON response """
        return Response(serializer.data)


class RateUserView(CreateAPIView):
    serializer_class = RateUserSerializer
    permission_classes = [IsAuthenticated, IsRatingCreator]

    def get_profile(self, pk):
        return get_object_or_404(Profile, pk=pk)

    def get(self, request, pk, *args, **kwargs):
        profile = self.get_profile(pk)

        """ Serialize the requested profile """
        profile_serializer = BaseProfileSerializer(
            profile, context={'request': request})

        """ Combine the serialized data """
        data = {
            'profile': profile_serializer.data
        }

        return Response(data)

    def create(self, request, pk, *args, **kwargs):
        profile = self.get_profile(pk)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        """ Check if the user is trying to rate their own profile """
        if profile.owner == request.user:
            raise PermissionDenied("You cannot rate your own profile.")

        """ Get the rated user (owner of the profile) """
        rate_user = profile.owner

        """ Create the rating """
        rating = Rating.objects.create(
            rating=serializer.validated_data.get('rating'),
            comment=serializer.validated_data.get('comment'),
            rate_user=rate_user,
            created_by=request.user
        )

        """ Add the rating to the rated user's profile """
        profile.ratings.add(rating)

        """ Recalculate average rating """
        ratings = profile.ratings.all()
        average_rating = sum([r.rating for r in ratings]) / len(ratings)
        profile.average_rating = average_rating
        profile.save()

        return Response({"message": "Rating submitted successfully."}, status=status.HTTP_201_CREATED)


class ProfileRatingAPIView(generics.ListAPIView):
    serializer_class = RatingSerializer

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter
    ]

    search_fields = [
        'comment',
    ]

    ordering_fields = [
        'rating',
        'created_at',
    ]

    def get_queryset(self):
        """ Get the profile object """
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])

        """ Get all ratings related to this profile """
        ratings = profile.ratings.all()

        return ratings


class RatingEditAPIView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated, IsRatingCreator]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        """
        After updating the rating, recalculate the average rating of the associated profile 
        """
        try:
            """
            Relate to the ForeignKey field is named 'rate_user' 
            """
            rate_user = instance.rate_user

            profile = rate_user.profile
        except (AttributeError, Profile.DoesNotExist):
            raise Http404("Associated profile not found for this rating.")
        self.update_average_rating(profile)
        return Response({'message': 'Rating updated successfully'}, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

    def update_average_rating(self, profile):
        """ Calculate the average rating for the profile """
        average_rating = profile.ratings.aggregate(Avg('rating'))[
            'rating__avg']

        """ Round the average rating to the nearest decimal or half decimal """
        if average_rating is not None:
            if average_rating % 1 < 0.25:
                average_rating = int(average_rating)
            elif average_rating % 1 < 0.75:
                average_rating = int(average_rating) + 0.5
            else:
                average_rating = int(average_rating) + 1

        """ Update the average_rating field of the profile """
        profile.average_rating = average_rating or 0
        profile.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        profile = instance.rate_user.profile
        self.perform_destroy(instance)
        ratings_count = profile.ratings.count()
        if ratings_count > 0:
            self.update_average_rating(profile)
        else:
            profile.average_rating = 0.0
            profile.save()
        return Response({'message': 'Rating deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class EmployeeProfileView(APIView):
    """
    Employee Profile view.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles_employee = Profile.objects.filter(profile_type='employee')
        serializer = EmployeeProfileSerializer(
            profiles_employee, many=True, context={'request': request})

        return Response(serializer.data)


class EmployeeProfileDetail(APIView):
    """
    Employee Profile get by id, if id does not exist return a http 404 error.
    """
    serializer_class = EmployeeProfileSerializer
    permission_classes = [IsOwnerReadOnly]

    def get_object(self, pk):
        try:
            employeeProfile = Profile.objects.get(
                profile_type='employee', pk=pk)
            self.check_object_permissions(self.request, employeeProfile)
            return employeeProfile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        employeeProfile = self.get_object(pk)
        serializer = EmployeeProfileSerializer(
            employeeProfile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        employeeProfile = self.get_object(pk)
        serializer = EmployeeProfileSerializer(
            employeeProfile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployerProfileView(APIView):
    """
    Employer Profile view.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles_employer = Profile.objects.filter(profile_type='employer')
        serializer = EmployerProfileSerializer(
            profiles_employer, many=True, context={'request': request})

        return Response(serializer.data)


class EmployerProfileDetail(APIView):
    """
    Employer Profile get by id, if id does not exist return a http 404 error.
    """
    serializer_class = EmployerProfileSerializer
    permission_classes = [IsOwnerReadOnly]

    def get_object(self, pk):
        try:
            employerProfile = Profile.objects.get(
                profile_type='employer', pk=pk)
            self.check_object_permissions(self.request, employerProfile)
            return employerProfile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        employerProfile = self.get_object(pk)
        serializer = EmployerProfileSerializer(
            employerProfile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        employerProfile = self.get_object(pk)
        serializer = EmployerProfileSerializer(
            employerProfile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminProfileView(APIView):
    """
    Admin Profile view.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profiles_admin = Profile.objects.filter(profile_type='admin')
        serializer = AdminProfileSerializer(
            profiles_admin, many=True, context={'request': request})

        return Response(serializer.data)


class AdminProfileDetail(APIView):
    """
    Admin Profile get by id, if id does not exist return a http 404 error.
    """
    serializer_class = AdminProfileSerializer
    permission_classes = [IsOwnerReadOnly]

    def get_object(self, pk):
        try:
            adminProfile = Profile.objects.get(profile_type='admin', pk=pk)
            self.check_object_permissions(self.request, adminProfile)
            return adminProfile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        adminProfile = self.get_object(pk)
        serializer = AdminProfileSerializer(
            adminProfile, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        adminProfile = self.get_object(pk)
        serializer = AdminProfileSerializer(
            adminProfile, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
