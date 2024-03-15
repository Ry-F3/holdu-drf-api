from rest_framework import serializers
from .models import Profile
from .models import Rating


class BaseProfileSerializer(serializers.ModelSerializer):
    """
    Extend the base profile serializer to divide the 
    application into three profile types.
    """
    owner_username = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    profile_type_display = serializers.ChoiceField(
        choices=Profile.PROFILE_CHOICES, source='get_profile_type_display', read_only=True)
    average_rating = serializers.ReadOnlyField()
    ratings = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request:
            return request.user == obj.owner
        return False

    """
    Ensure ratings are read only
    """

    def get_ratings(self, obj):
        return obj.ratings.values_list('id', flat=True)

    class Meta:
        model = Profile
        fields = ['id', 'owner_username', 'created_at',
                  'updated_at', 'name', 'content', 'image', 'is_owner', 'average_rating', 'ratings', 'profile_type_display']


class EmployeeProfileSerializer(BaseProfileSerializer):

    class Meta(BaseProfileSerializer.Meta):
        fields = BaseProfileSerializer.Meta.fields


class EmployerProfileSerializer(BaseProfileSerializer):

    class Meta(BaseProfileSerializer.Meta):
        fields = BaseProfileSerializer.Meta.fields


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
    # Rename 'id' field to 'id_for_rating'
    id_for_rating = serializers.IntegerField(source='id')

    class Meta:
        model = Rating
        fields = ['created_by', 'id_for_rating', 'rate_user',
                  'rating', 'comment', 'created_at', 'updated_at']

    def get_created_by(self, obj):
        if obj.created_by:
            # Get the created_by profile data
            profile = obj.created_by.profile
            # Check the profile_type to determine the appropriate serializer
            if profile.profile_type == 'employee':
                profile_serializer = EmployeeProfileSerializer(profile)
            elif profile.profile_type == 'employer':
                profile_serializer = EmployerProfileSerializer(profile)
            else:
                return None
            # Retrieve the serialized data including the image field
            profile_data = profile_serializer.data
            return profile_data
        return None
