from django.contrib import admin
from .models import Report
import json
from django.utils.safestring import mark_safe

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('generated_by', 'generated_at', 'formatted_report_data')
    list_filter = ('generated_at', 'generated_by')
    search_fields = ('generated_by__username',)
    ordering = ('-generated_at',)
    readonly_fields = ('generated_by', 'generated_at', 'formatted_report_data')

    def formatted_report_data(self, obj):
        if obj.report_data:
            formatted_data = json.dumps(obj.report_data, indent=4)
            return mark_safe(f'<pre>{formatted_data}</pre>')
        return "No data available"
    formatted_report_data.short_description = "Report Data"

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True