from django.contrib import admin
from .models import WorkExperience


class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('owner', 'job_title', 'company_name',
                    'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')
    search_fields = ('owner__username', 'job_title', 'company_name')
    readonly_fields = ('owner',)
    date_hierarchy = 'start_date'


admin.site.register(WorkExperience, WorkExperienceAdmin)
