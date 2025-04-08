from django.contrib import admin
from .models import Proposal

@admin.register(Proposal)
class ProposalAdmin(admin.ModelAdmin):
    list_display = ('title', 'grant_call', 'applicant', 'evaluator', 'status', 'submitted_at')
    list_filter = ('status', 'grant_call', 'submitted_at')
    search_fields = ('title', 'description', 'applicant__username', 'evaluator__username', 'grant_call__title')
    ordering = ('-submitted_at',)
    readonly_fields = ('submitted_at',)
    list_editable = ('status', 'evaluator')