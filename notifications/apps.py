from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

    def ready(self):
        import notifications.signals

    """
    Instructions to initiate signals.py from:
    https://www.geeksforgeeks.org/how-to-create-and-use-signals-in-django/ 
   
    """
