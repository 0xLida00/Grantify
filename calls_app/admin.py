from django.contrib import admin
from .models import GrantCall, GrantQuestion, GrantChoice, GrantResponse

@admin.register(GrantCall)
class GrantCallAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'budget', 'created_by', 'created_at', 'modified_at')
    list_filter = ('status', 'created_at', 'modified_at', 'deadline')
    search_fields = ('title', 'description', 'eligibility', 'created_by__username')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'modified_at')
    filter_horizontal = ('favorited_by',)

@admin.register(GrantQuestion)
class GrantQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'grant_call', 'question_type')
    list_filter = ('question_type', 'grant_call')
    search_fields = ('question_text', 'grant_call__title')
    ordering = ('grant_call',)

@admin.register(GrantChoice)
class GrantChoiceAdmin(admin.ModelAdmin):
    list_display = ('choice_text', 'question')
    search_fields = ('choice_text', 'question__question_text')
    ordering = ('question',)

@admin.register(GrantResponse)
class GrantResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'grant_call', 'question', 'is_final_submission', 'created_at', 'updated_at')
    list_filter = ('is_final_submission', 'created_at', 'updated_at')
    search_fields = ('user__username', 'grant_call__title', 'question__question_text', 'response')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')