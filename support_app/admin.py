from django.contrib import admin
from .models import SupportTicket, Feedback, FAQ, ToDo

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'priority', 'status', 'response', 'created_at', 'updated_at')
    list_filter = ('priority', 'status', 'created_at', 'updated_at')
    search_fields = ('subject', 'description', 'user__username', 'response')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    list_editable = ('status', 'priority', 'response')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'status', 'thumbs_up', 'thumbs_down', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('question', 'answer')
    ordering = ('-created_at',)
    readonly_fields = ('thumbs_up', 'thumbs_down', 'created_at')
    list_editable = ('status',)

@admin.register(ToDo)
class ToDoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'completed', 'due_date', 'created_at')
    list_filter = ('completed', 'due_date', 'created_at')
    search_fields = ('title', 'description', 'user__username')