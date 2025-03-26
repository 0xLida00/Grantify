from django.db import models
from accounts_app.models import CustomUser
from calls_app.models import GrantCall

class Proposal(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('feedback', 'Feedback Provided'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    grant_call = models.ForeignKey(GrantCall, on_delete=models.CASCADE, related_name="proposals")
    applicant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="proposals")
    title = models.CharField(max_length=255)
    description = models.TextField()
    document = models.FileField(upload_to="proposals/")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title