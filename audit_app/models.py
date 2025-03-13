# audit_app/models.py
from django.db import models
from accounts_app.models import CustomUser

class LogEntry(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="log_entries")
    action = models.CharField(max_length=255)
    object_repr = models.CharField(max_length=255)
    change_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"LogEntry: {self.action} by {self.user if self.user else 'System'}"