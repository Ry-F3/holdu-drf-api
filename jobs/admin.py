from django.contrib import admin
from .models import Job, Application


class ApplicationInline(admin.TabularInline):
    model = Application
    extra = 0


class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'employer_profile',
                    'closing_date', 'created_at', 'updated_at')
    list_filter = ('closing_date', 'created_at', 'updated_at')
    search_fields = ('title', 'location', 'employer_profile__owner__username')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ApplicationInline]


admin.site.register(Job, JobAdmin)
