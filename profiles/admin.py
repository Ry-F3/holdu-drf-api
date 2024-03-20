from django.contrib import admin
from .models import Profile, Rating


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['owner', 'profile_type', 'created_at', 'updated_at']
    list_filter = ['profile_type']
    search_fields = ['owner__username', 'owner__email']


admin.site.register(Profile, ProfileAdmin)


class RatingAdmin(admin.ModelAdmin):
    list_display = ('rating', 'rate_user', 'created_by', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('rate_user__username', 'created_by__username')
    date_hierarchy = 'created_at'


admin.site.register(Rating, RatingAdmin)
