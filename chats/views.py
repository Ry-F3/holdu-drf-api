from rest_framework import generics, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Chat, Message
from .serializers import ChatSerializer, MessageSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from drf_api.permissions import IsOwnerOrSender


class ChatListCreateAPIView(generics.ListCreateAPIView):
    """
    View to handle listing and creating chat instances.

    This view receives incoming requests from users who want
    to list existing chats or create new ones.
    """
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrSender]

    filter_backends = [filters.SearchFilter]
    search_fields = ['sender__username', 'recipient__username']

    def post(self, request, *args, **kwargs):
        """
        Handle creating a new chat instance.

        This method is called when a user submits a request to
        create a new chat.
        It checks if the required information
        (like the recipient ID and message content) is provided,
        verifies if the chat or message already exists,
        and then proceeds to create a new chat or message accordingly.
        """
        recipient_id = request.data.get('recipient')
        content = request.data.get('content')
        sender = request.user

        if not recipient_id:
            return Response({'error': 'Recipient ID is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        recipient = get_object_or_404(User, pk=recipient_id)

        existing_chat = Chat.objects.filter(
            sender=sender, recipient=recipient).first()

        if existing_chat:
            """ Check if the message already exists in the chat """
            existing_message = existing_chat.messages.filter(
                content=content, sender=sender).first()
            if existing_message:
                return Response({'error': 'Message already sent in this chat'},
                                status=status.HTTP_400_BAD_REQUEST)

            """ If a chat already exists, create a new message within it """
            message = Message.objects.create(
                chat=existing_chat, sender=sender,
                recipient=recipient, content=content)
            """ Pass request to serializer context """
            serializer = ChatSerializer(
                existing_chat, context={'request': request})
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        """ If no chat exists, create a new chat and message """
        serializer = ChatSerializer(
            data={'sender': sender.id,
                  'recipient': recipient.id, 'content': content},
            context={
                'request': request})  # Pass request to serializer context
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChatDetailAPIView(generics.RetrieveDestroyAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]
