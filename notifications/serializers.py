from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'owner', 'sender', 'sent_at',
                  'category', 'is_read', 'title', 'content']
        read_only_fields = ['id', 'owner', 'sent_at',
                            'is_read']
