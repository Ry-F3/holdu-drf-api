from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from connections.models import Connection
from jobs.models import Job
from chats.models import Message
from django.contrib.auth import get_user_model

"""
Instructions for signals.py from:
https://www.geeksforgeeks.org/how-to-create-and-use-signals-in-django/ 
Code heavily inspired by: https://github.com/nacht-falter/sonic-explorers-api
I have made alterations to make it fit my project and models.
"""

User = get_user_model()


def create_notification(**kwargs):
    Notification.objects.create(
        owner=kwargs["owner"],
        sender=kwargs["sender"],
        category=kwargs["category"],
        item_id=kwargs["item_id"],
        title=kwargs["title"],
        content=kwargs["content"],
    )


@receiver(post_save, sender=Connection)
def connection_notification(sender, instance, created, **kwargs):
    if created:
        print("Connection created. Owner:", instance.owner,
              "Connection:", instance.connection)
        if instance.accepted:
            print("Connection request accepted. Owner:",
                  instance.owner, "Connection:", instance.connection)
            # Notification to the owner of the connection
            owner_notification_data = {
                "owner": instance.owner,
                "sender": instance.owner,
                "title": "You have a new Connection!",
                "category": 'connection_accepted',
                "content": f'You are now connected to {instance.connection.username}.',
                "item_id": instance.id
            }
            create_notification(**owner_notification_data)
            # Notification to the sender of the connection
            sender_notification_data = {
                "owner": instance.connection,
                "sender": instance.owner,
                "title": f"Connection request accepted by {instance.owner.username}!",
                "category": 'connection_accepted',
                "content": f'Your connection request to {instance.owner.username} has been accepted.',
                "item_id": instance.id
            }
            create_notification(**sender_notification_data)
        else:
            print("Connection request sent. Owner:",
                  instance.connection, "Connection:", instance.owner)
            data = {
                "owner": instance.connection,
                "sender": instance.owner,
                "title": f"You have a new Connection request from {instance.owner.username}!",
                "category": 'connection_request',
                "content": f'{instance.owner.username} sent you a connection request.',
                "item_id": instance.id
            }
            create_notification(**data)


@receiver(post_save, sender=Message)
def message_alert(sender, instance, created, **kwargs):
    if created:
        # Create a message alert notification
        data = {
            "owner": instance.recipient,
            "sender": instance.sender,
            "title": "New Message",
            "category": 'message_alert',
            "content": f"You have received a new message from {instance.sender.username}.",
            "item_id": instance.id
        }
        create_notification(**data)


@receiver(post_save, sender=Job)
def new_job_notification(sender, instance, created, **kwargs):
    if created:
        print("New job created. Employer:", instance.employer_profile.owner)
        print("Profile type of employer:",
              instance.employer_profile.profile_type)
        if instance.employer_profile.profile_type == 'employee':
            print("Sending notification to employee:",
                  instance.employer_profile.owner)
            data = {
                "owner": instance.employer_profile.owner,
                "sender": instance.employer_profile.owner,
                "title": "New Job Opportunity",
                "category": 'new_job',
                "content": f"New job opportunity: {instance.title} at {instance.employer_profile}.",
                "item_id": instance.id
            }
            create_notification(**data)
