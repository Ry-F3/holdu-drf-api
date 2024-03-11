from rest_framework import serializers
from .models import Profile


class BaseProfileSerializer(serializers.ModelSerializer):
    """
    Extend the base profile serializer to divide the 
    application into three profile types.
    """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()

    def get_is_owner(self, obj):
        request = self.context['request']
        return request.user == obj.owner

    class Meta:
        model = Profile
        fields = ['id', 'owner', 'created_at',
                  'updated_at', 'name', 'content', 'image', 'is_owner']


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
