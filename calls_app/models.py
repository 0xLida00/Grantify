# calls_app/models.py
from django.db import models
from accounts_app.models import CustomUser

class GrantCall(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    eligibility = models.TextField()
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="grant_calls")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title