from rest_framework import serializers
from .models import Profile
from .models import Rating


class BaseProfileSerializer(serializers.ModelSerializer):
    """
    Extend the base profile serializer to divide the 
    application into three profile types.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request:
            return request.user == obj.owner
        return False

    class Meta:
        model = Profile
        fields = ['id', 'owner', 'created_at',
                  'updated_at', 'name', 'content', 'image', 'is_owner', 'average_rating', 'ratings']


class EmployeeProfileSerializer(BaseProfileSerializer):
    profile_type = serializers.CharField(
        source='get_profile_type_display', read_only=True)

    class Meta(BaseProfileSerializer.Meta):
        fields = BaseProfileSerializer.Meta.fields + ['profile_type']


class EmployerProfileSerializer(BaseProfileSerializer):
    profile_type = serializers.CharField(
        source='get_profile_type_display', read_only=True)

    class Meta(BaseProfileSerializer.Meta):
        fields = BaseProfileSerializer.Meta.fields + ['profile_type']


class AdminProfileSerializer(BaseProfileSerializer):
    profile_type = serializers.CharField(
        source='get_profile_type_display', read_only=True)

    class Meta(BaseProfileSerializer.Meta):
        fields = BaseProfileSerializer.Meta.fields + \
            ['profile_type']


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

    class Meta:
        model = Rating
        fields = ['created_by', 'id', 'rate_user',
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
