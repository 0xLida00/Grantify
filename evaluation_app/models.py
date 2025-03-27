from django.db import models
from accounts_app.models import CustomUser
from proposals_app.models import Proposal

class Evaluation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    )

    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name="evaluations")
    evaluator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="evaluations")
    score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    evaluated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Evaluation for {self.proposal.title} by {self.evaluator.username}"