from django.contrib import admin
from .models import Connection


class ConnectionAdmin(admin.ModelAdmin):
    list_display = ('owner', 'connection', 'created_at', 'accepted')
    list_filter = ('created_at', 'accepted')
    search_fields = ('owner__username', 'connection__username')
    readonly_fields = ('created_at',)


admin.site.register(Connection, ConnectionAdmin)
