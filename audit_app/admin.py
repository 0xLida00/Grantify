from django.contrib import admin
from .models import LogEntry

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action', 'user', 'log_level', 'source', 'created_at')
    list_filter = ('log_level', 'source', 'created_at')
    search_fields = ('action', 'user__username', 'change_message', 'object_repr')
    ordering = ('-created_at',)
    readonly_fields = ('user', 'action', 'object_repr', 'change_message', 'log_level', 'source', 'created_at')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False