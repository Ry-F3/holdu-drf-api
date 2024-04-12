from rest_framework import generics, permissions
from .models import Connection
from rest_framework.response import Response
from rest_framework import status
from .serializers import ConnectionSerializer
from drf_api.permissions import IsOwnerReadOnly


class ConnectionList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConnectionSerializer

    def get_queryset(self):
        """Filter connections by the owner and accepted status"""
        return Connection.objects.filter(
            owner=self.request.user)

    def perform_create(self, serializer):
        """Create a new connection"""
        serializer.save(owner=self.request.user)
        return Response({"message": "Connection request sent"},
                        status=status.HTTP_201_CREATED)


class AcceptedConnectionList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConnectionSerializer

    def get_queryset(self):
        """Retrieve accepted connections"""
        return Connection.objects.filter(
            owner=self.request.user, accepted=True)


class PendingConnectionList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ConnectionSerializer

    def get_queryset(self):
        """Retrieve pending connections"""
        return Connection.objects.filter(
            connection=self.request.user, accepted=False)


class ConnectionDetail(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated,
                          IsOwnerReadOnly]
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer

    def delete(self, request, *args, **kwargs):
        """Delete a connection"""
        connection = self.get_object()
        connection.delete()

        """Check if a reverse connection exists"""
        reverse_connection = Connection.objects.filter(
            owner=connection.connection,
            connection=connection.owner).first()

        if not reverse_connection:
            """
            If reverse connection doesn't exist,
            check if there's a connection with the same users but flipped
            """
            reverse_connection = Connection.objects.filter(
                owner=connection.owner,
                connection=connection.connection).first()

        if reverse_connection:
            """If reverse connection exists, delete it as well"""
            reverse_connection.delete()

        return Response({"message": "Connection deleted"},
                        status=status.HTTP_204_NO_CONTENT)


class AcceptConnection(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer

    def put(self, request, *args, **kwargs):
        """Accept a connection"""
        connection = self.get_object()
        connection.accepted = True
        connection.save()

        """Check if a reverse connection already exists"""
        reverse_connection = Connection.objects.filter(
            owner=connection.connection, connection=connection.owner).first()

        if reverse_connection:
            """If reverse connection exists, update its accepted field"""
            reverse_connection.accepted = True
            reverse_connection.save()
        else:
            """If reverse connection doesn't exist, create it"""
            reverse_connection = Connection.objects.create(
                owner=connection.connection,
                connection=connection.owner, accepted=True)

        return Response({"message": "Connection request accepted"},
                        status=status.HTTP_200_OK)


class DeclineConnection(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer

    def delete(self, request, *args, **kwargs):
        """Decline a connection"""
        connection = self.get_object()
        connection.delete()

        """Check if a reverse connection exists"""
        reverse_connection = Connection.objects.filter(
            owner=connection.connection,
            connection=connection.owner).first()

        if not reverse_connection:
            """If reverse connection doesn't exist,
            check if there's a connection with the same users but flipped"""
            reverse_connection = Connection.objects.filter(
                owner=connection.owner,
                connection=connection.connection).first()

        if reverse_connection:
            """If reverse connection exists, delete it as well"""
            reverse_connection.delete()

        return Response({"message": "Connection request declined"},
                        status=status.HTTP_204_NO_CONTENT)
