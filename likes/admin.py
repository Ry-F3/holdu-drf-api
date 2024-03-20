from django.contrib import admin
from .models import Like


class LikeAdmin(admin.ModelAdmin):
    list_display = ('owner', 'job', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('owner__username', 'job__title')
    readonly_fields = ('created_at',)


admin.site.register(Like, LikeAdmin)
