from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('owner', 'sender', 'sent_at',
                    'category', 'is_read', 'content')
    list_filter = ('category', 'is_read', 'sent_at')
    search_fields = ('owner__username', 'sender__username', 'content')
    readonly_fields = ('sent_at',)


admin.site.register(Notification, NotificationAdmin)
