from rest_framework import serializers
from .models import Like
from django.db import IntegrityError


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer used for the Like model
    The create method handles the unique constraint on 'owner' and 'job'
    Please note: code has been mostly used from CI's walkthrough project.
    """
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Like
        fields = ['id', 'created_at', 'owner', 'job']

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError("You already liked this job.")
