from django.db import models
from accounts_app.models import CustomUser

class Report(models.Model):
    generated_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)
    report_data = models.JSONField()

    def __str__(self):
        return f"Report generated on {self.generated_at}"

    def get_formatted_data(self):
        return self.report_data