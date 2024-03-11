from rest_framework import serializers
from .models import Profile


class BaseProfileSerializer(serializers.ModelSerializer):
    """
    Extend the base profile serializer to divide the 
    application into three profile types.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Profile
        fields = ['id', 'owner', 'created_at',
                  'updated_at', 'name', 'content', 'image']


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
        fields = BaseProfileSerializer.Meta.fields + ['profile_type']
