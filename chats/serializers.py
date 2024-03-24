from rest_framework import serializers
from .models import Chat, Message
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturaltime


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for handling User instances.

    """
    class Meta:
        model = User
        fields = ['id', 'username']


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for handling message instances.

    """
    sender_name = serializers.SerializerMethodField()
    recipient_name = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'sender_name', 'recipient',
                  'recipient_name', 'timestamp', 'content']
        read_only_fields = ['sender']

    def get_timestamp(self, obj):
        return naturaltime(obj.timestamp)

    def get_sender_name(self, obj):
        return obj.sender.username if obj.sender else None

    def get_recipient_name(self, obj):
        return obj.recipient.username if obj.recipient else None


class ChatSerializer(serializers.ModelSerializer):
    """
    Serializer for handling chat instances.

    Methods:
    - create(validated_data): Creates a new chat instance
    based on the validated data received from the view.
    """
    chat_id = serializers.IntegerField(source='id', read_only=True)
    sender_name = serializers.SerializerMethodField()
    recipient_name = serializers.SerializerMethodField()
    messages = MessageSerializer(many=True, read_only=True)
    content = serializers.CharField(write_only=True)

    class Meta:
        model = Chat
        fields = ['chat_id', 'sender', 'sender_name', 'recipient',
                  'recipient_name', 'timestamp', 'content', 'messages']
        read_only_fields = ['sender', 'chat_id']

    def get_sender_name(self, obj):
        return obj.sender.username if obj.sender else None

    def get_recipient_name(self, obj):
        return obj.recipient.username if obj.recipient else None

    def create(self, validated_data):
        """
        Create a new chat instance or add a message to an existing chat.
        This method handles the creation of a new chat instance or
        the addition of a message to an existing chat
        based on the validated data received from the view.
        If a chat already exists between the sender and recipient,
        the message is added to that chat. If no chat exists,
        a new chat instance is created along with a message.
        """
        content = validated_data.pop('content')
        recipient = validated_data.pop('recipient')
        sender = self.context['request'].user
        # Get authenticated user

        """ Check if there's an existing chat between
        sender and recipient
        """
        existing_chat = Chat.objects.filter(
            sender=sender, recipient=recipient).first()

        if existing_chat:
            """ Check if the message already exists
            within the chat
            """
            if existing_chat.messages.filter(content=content).exists():
                raise serializers.ValidationError(
                    "Message already exists in the chat.")

            """ If a chat already exists, create a new
            message within it
            """
            message = Message.objects.create(
                chat=existing_chat, sender=sender,
                recipient=recipient, content=content)
            return existing_chat
        else:
            """ If no chat exists, check if the recipient
            has initiated a chat
            """
            existing_chat = Chat.objects.filter(
                sender=recipient, recipient=sender).first()

            if existing_chat:
                """ Check if the message already exists
                within the chat
                """
                if existing_chat.messages.filter(content=content).exists():
                    raise serializers.ValidationError(
                        "Message already exists in the chat.")

                """ If the recipient initiated the chat,
                add the message to that chat
                """
                message = Message.objects.create(
                    chat=existing_chat, sender=sender,
                    recipient=recipient, content=content)
                return existing_chat
            else:
                """ If no chat exists, create a new
                chat and message
                """
                chat = Chat.objects.create(
                    sender=sender, recipient=recipient, **validated_data)
                message = Message.objects.create(
                    chat=chat, sender=sender,
                    recipient=recipient, content=content)
                return chat
