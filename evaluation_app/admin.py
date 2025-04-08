from django.contrib import admin
from .models import Evaluation

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    list_display = ('proposal', 'evaluator', 'score', 'status', 'evaluated_at')
    list_filter = ('status', 'evaluated_at', 'evaluator')
    search_fields = ('proposal__title', 'evaluator__username', 'feedback')
    ordering = ('-evaluated_at',)
    readonly_fields = ('evaluated_at',)

    def has_add_permission(self, request):
        return False