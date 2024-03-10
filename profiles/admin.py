from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['owner', 'profile_type', 'created_at', 'updated_at']
    list_filter = ['profile_type']
    search_fields = ['owner__username', 'owner__email']


admin.site.register(Profile, ProfileAdmin)
