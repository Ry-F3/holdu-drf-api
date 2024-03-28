from rest_framework import serializers
from .models import Profile
from .models import Rating
from connections.models import Connection
from django.contrib.auth.models import User


class BaseProfileSerializer(serializers.ModelSerializer):
    """
    Extend the base profile serializer to divide the
    application into three profile types.
    """
    owner_username = serializers.ReadOnlyField(source='owner.username')
    owner_id = serializers.ReadOnlyField(source='owner.id')
    is_owner = serializers.SerializerMethodField()
    average_rating = serializers.ReadOnlyField()
    ratings = serializers.SerializerMethodField()
    connections_id = serializers.SerializerMethodField(read_only=True)
    connections_count = serializers.ReadOnlyField()
    likes_count = serializers.ReadOnlyField()

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request:
            return request.user == obj.owner
        return False

    def get_connections_id(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            connections = obj.owner.user_connected.filter(accepted=True)
            return [connection.connection_id
                    for connection in connections]
        return None

    """
    Ensure ratings are read only
    """

    def get_ratings(self, obj):
        return obj.ratings.values_list('id', flat=True)

    class Meta:
        model = Profile
        fields = ['id', 'owner_username',  'owner_id', 'created_at',
                  'updated_at', 'name', 'content', 'image', 'is_owner',
                  'average_rating', 'ratings',
                  'connections_count', 'connections_id',
                  'likes_count', 'profile_type']


class EmployeeProfileSerializer(BaseProfileSerializer):
    class Meta(BaseProfileSerializer.Meta):
        fields = [
            field for field in BaseProfileSerializer.Meta.fields
            if field != 'connections_id'
        ]


class EmployerProfileSerializer(BaseProfileSerializer):
    class Meta(BaseProfileSerializer.Meta):
        fields = [
            field for field in BaseProfileSerializer.Meta.fields
            if field != 'connections_id'
        ]


class AdminProfileSerializer(BaseProfileSerializer):

    class Meta(BaseProfileSerializer.Meta):
        fields = BaseProfileSerializer.Meta.fields


class RateUserSerializer(serializers.Serializer):
    RATINGS_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]

    rating = serializers.ChoiceField(choices=RATINGS_CHOICES)
    comment = serializers.CharField(max_length=255)


class RatingSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    """ Rename 'id' field to 'id_for_rating' """
    id_for_rating = serializers.IntegerField(source='id')

    class Meta:
        model = Rating
        fields = ['created_by', 'id_for_rating', 'rate_user',
                  'rating', 'comment', 'created_at', 'updated_at']

    def get_created_by(self, obj):
        """ Display data for created_by """
        profile_serializer = BaseProfileSerializer()
        if obj.created_by:
            """ Get the created_by profile data """
            profile = obj.created_by.profile
            """
            Check the profile_type to determine the appropriate serializer
            """
            if profile.profile_type == 'employee':
                profile_serializer = EmployeeProfileSerializer(profile)
            elif profile.profile_type == 'employer':
                profile_serializer = EmployerProfileSerializer(profile)
            else:
                return None
            """
            Retrieve the serialized data including the image field
            """
            profile_data = profile_serializer.data
            return profile_data
        return None
