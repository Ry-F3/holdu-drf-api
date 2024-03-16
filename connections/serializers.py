from django.db import IntegrityError
from rest_framework import serializers
from .models import Connection


class ConnectionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    connection_name = serializers.ReadOnlyField(source='connection.username')

    class Meta:
        model = Connection
        fields = ['id', 'owner', 'created_at',
                  'connection', 'connection_name', 'accepted']
        # Make the 'accepted' field read-only by default
        read_only_fields = ['accepted']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Check if the serializer is used for creating a new connection
        if self.context.get('request') and hasattr(self.context['request'], 'method'):
            request_method = self.context['request'].method
            if request_method == 'POST':  # If the request is for creating a new connection
                # Remove the 'accepted' field from the form
                self.fields.pop('accepted', None)

    def create(self, validated_data):
        # Check if owner and connection are the same user
        if validated_data['owner'] == validated_data['connection']:
            raise serializers.ValidationError(
                {'detail': "You can't connect with yourself."})

        # Check if the connection already exists
        existing_connection = Connection.objects.filter(
            owner=validated_data['owner'], connection=validated_data['connection']).exists()
        if existing_connection:
            raise serializers.ValidationError(
                {'detail': 'You have already made this connection.'})

        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(
                {'detail': 'Possible duplicate or integrity error.'})
