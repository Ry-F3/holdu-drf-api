from django.http import Http404
from rest_framework.exceptions import NotFound, PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import status, generics, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile, Rating
from rest_framework.permissions import IsAuthenticated
from drf_api.permissions import IsOwnerReadOnly, IsRatingCreator
from django.db.models import Avg, Count, Q
from rest_framework.generics import (
    CreateAPIView, RetrieveUpdateAPIView, RetrieveAPIView,
    UpdateAPIView, DestroyAPIView
)
from .serializers import (
    RateUserSerializer,
    BaseProfileSerializer, RatingSerializer,
)


class ProfilesView(generics.ListAPIView):
    """
    View to retrieve all profiles.
    """
    serializer_class = BaseProfileSerializer
    queryset = Profile.objects.annotate(
        likes_count=Count('owner__like', distinct=True),
        connections_count=Count('owner__connections', filter=Q(
            owner__connections__accepted=True), distinct=True)
    ).order_by('-created_at')

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
        'connections_count',
        'likes_count',

    ]

    def get(self, request, *args, **kwargs):
        """
        Get the queryset based on search and ordering
        """
        queryset = self.filter_queryset(self.get_queryset())

        """
        Serialize the queryset using the serializer class
        """
        serializer = self.serializer_class(
            queryset, many=True, context={'request': request})

        """
        Return the serialized data in JSON response
        """
        return Response(serializer.data)

    def get_serializer_context(self):
        """
        Add the request object to the serializer's context.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class ProfileDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Profile detail view.
    """
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = BaseProfileSerializer


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

        return Response(
            {"message": "Rating submitted successfully."},
            status=status.HTTP_201_CREATED)


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
        profile_id = self.kwargs.get('pk')
        queryset = Rating.objects.filter(rate_user__profile__id=profile_id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class RatingEditAPIView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated, IsRatingCreator]

    def get_serializer_context(self):
        """
        Add the request object to the serializer's context.
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        """
        After updating the rating, recalculate the average
        rating of the associated profile
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
        return Response({'message': 'Rating updated successfully'},
                        status=status.HTTP_200_OK)

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
        return Response({'message': 'Rating deleted successfully'},
                        status=status.HTTP_204_NO_CONTENT)
